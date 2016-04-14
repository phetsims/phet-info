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
    
    var thisNode = this;

    // Add observers to observables provided by the client.
    var valueObserver = function( value ) { /* ... */ };
    valueProperty.link( valueObserver );

    var enabledObserver = function( enabled ) { /* ... */ };
    options.enabledProperty.link( enabledObserver );
    
    var changedListener = function() { /* ... */ };
    changedEmitter.addListener( changedListener );
    
    var someStateListener = function() { /* ... */ };
    stateEvents.on( 'someState', someStateListener );

    // @public Properties owned by this instance
    this.myPublicProperty = new Property( 0 );
    this.myEmitter = new Emitter();
    this.myEvents = new Events();

    // @private
    var myDerivedProperty = new DerivedProperty( [ valueProperty ], function( value ) { /*...*/ } );

    Node.call( this );

    // register with tandem
    options.tandem && options.tandem.addInstance( this );
    
    // @private
    this.disposeDisposeExampleNode = function() {
      
      // observables provided by the client
      valueProperty.unlink( valueObserver );
      options.enabledProperty.unlink( enabledObserver );
      changedEmitter.removeListener( changedListener );
      stateEvents.off( 'someState', someStateListener );
      
      // observables owned by this instance that are part of the public interface
      thisNode.myPublicProperty.dispose();
      thisNode.myEmitter.dispose();
      thisNode.myEvents.dispose();

      // observables owned by this instance that are private
      myDerivedProperty.dispose();

      // de-register with tandem
      options.tandem && options.tandem.removeInstance( this );
    };
  }

  return inherit( Node, DisposeExampleNode, {
    
    // @public
    dispose: function() {
      this.disposeDisposeExampleNode();
      Node.prototype.dispose.call( this );
    }
  } );
} );
