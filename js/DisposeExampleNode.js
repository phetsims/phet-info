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
  function DisposeExampleNode( valueProperty, changedEmitter, stateEvents, options ) {

    options = _.extend( {
      enabledProperty: new Property( true ), // optionally provided by client
      tandem: null
    }, options );

    // @private
    this.disposeDisposeExampleNodeEmitter = new Emitter();

    // Add observers to observables provided by the client.
    valueProperty.linkWithDisposal( this.disposeDisposeExampleNodeEmitter, function( value ) {
      /* ... */
    } );

    options.enabledProperty.linkWithDisposal( this.disposeDisposeExampleNodeEmitter, function( enabled ) { /* ... */ } );

    changedEmitter.addListenerWithDisposal( this.disposeDisposeExampleNodeEmitter, function() { /* ... */ } );

    stateEvents.onWithDisposal( this.disposeDisposeExampleNodeEmitter, 'someState', function() { /* ... */ } );

    // @public Properties owned by this instance
    this.myPublicProperty = new Property( 0, { disposeExitter: this.disposeDisposeExampleNodeEmitter } );
    this.myEmitter = new Emitter( { disposeExitter: this.disposeDisposeExampleNodeEmitter } );
    this.myEvents = new Events( { disposeExitter: this.disposeDisposeExampleNodeEmitter } );

    // @private
    var myDerivedProperty = new DerivedProperty( [ valueProperty ], function( value ) { /*...*/ }, {
      disposeDisposeExampleNodeEmitter: this.disposeDisposeExampleNodeEmitter
    } );

    Node.call( this );

    // register with tandem
    options.tandem && options.tandem.addInstanceWithDisposal( this.disposeDisposeExampleNodeEmitter, this );
  }

  return inherit( Node, DisposeExampleNode, {

    // @public
    dispose: function() {
      this.disposeDisposeExampleNodeEmitter.emit();
      this.disposeDisposeExampleNodeEmitter.dispose();
      this.disposeDisposeExampleNodeEmitter = null; // so it would fail if dispose() called twice
      Node.prototype.dispose.call( this );
    }
  } );
} );
