// Copyright 2016, University of Colorado Boulder

/**
 * Example of the various situations related to dispose.
 * This example does not run, it's intended for discussion of patterns.
 * See https://github.com/phetsims/axon/issues/93
 *
 * @author Chris Malley (PixelZoom, Inc.)
 */
define( function( require ) {
  'use strict';

  // modules
  var DerivedProperty = require( 'AXON/DerivedProperty' );
  var Emitter = require( 'AXON/Emitter' );
  var Events = require( 'AXON/Events' );
  var inherit = require( 'PHET_CORE/inherit' );
  var Node = require( 'SCENERY/nodes/Node' );
  var Property = require( 'AXON/Property' );

  /**
   * @param {Property} valueProperty
   * @param {Emitter} changedEmitter
   * @param {Events} stateEvents
   * @param {Object} options
   * @constructor
   */
  function ExampleNode( valueProperty, changedEmitter, stateEvents, options ) {

    options = _.extend( {
      enabledProperty: new Property( true ), // optionally provided by client
      tandem: null
    }, options );

    // @private - Use a  class-specific name so it doesn't get shadowed by one in a subclass
    this.disposeExampleNodeEmitter = new Emitter();

    // nickname var for ease of readability for usages in the constructor
    var disposeEmitter = this.disposeExampleNodeEmitter;

    // Add observers to observables provided by the client.
    valueProperty.linkWithDisposal( disposeEmitter, function( value ) {
      /* ... */
    } );

    options.enabledProperty.linkWithDisposal( disposeEmitter, function( enabled ) { /* ... */ } );

    changedEmitter.addListenerWithDisposal( disposeEmitter, function() { /* ... */ } );

    stateEvents.onWithDisposal( disposeEmitter, 'someState', function() { /* ... */ } );

    // @public Properties owned by this instance
    this.myPublicProperty = Property.withDisposal( 0, disposeEmitter );
    this.myEmitter = Emitter.withDisposal( disposeEmitter );
    this.myEvents = Events.withDisposal( disposeEmitter );

    // @private
    var myDerivedProperty = DerivedProperty.withDisposal( [ valueProperty ], function( value ) { /*...*/ } );
    console.log( myDerivedProperty );

    Node.call( this );

    // register with tandem
    options.tandem && options.tandem.addInstanceWithDisposal( this, disposeEmitter );
  }

  return inherit( Node, ExampleNode, {

    // @public
    dispose: function() {
      this.disposeExampleNodeEmitter.emit();
      this.disposeExampleNodeEmitter.dispose();
      this.disposeExampleNodeEmitter = null; // so it would fail if dispose() called twice
      Node.prototype.dispose.call( this );
    }
  } );
} );
