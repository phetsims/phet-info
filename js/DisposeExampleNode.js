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

    Node.call( this ); // Node would be a Disposable, so this sets things up.

    // Add observers to observables provided by the client.
    valueProperty.link( function( value ) {}, { disposable: this } ); // Disposable as second argument

    changedEmitter.addListener( function() { /* ... */ }, { disposable: this } );

    stateEvents.on( 'someState', function() {}, { disposable: this } );

    // @public Properties owned by this instance
    this.myPublicProperty = new Property( 0, { disposable: this } );
    this.myEmitter = new Emitter( { disposable: this } );
    this.myEvents = new Events( { disposable: this } );

    // @private
    var myDerivedProperty = new DerivedProperty( [ valueProperty ], function( value ) { /* ... */ }, {
      disposable: this
    } );

    this.mutate( options );

    // register with tandem
    tandem.addInstance( this, { disposable: this } );
  }

  return inherit( Node, ExampleNode );
} );