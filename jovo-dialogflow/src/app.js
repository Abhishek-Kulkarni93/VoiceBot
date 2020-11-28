'use strict';

const { App } = require('jovo-framework');
const { GoogleAssistant } = require('jovo-platform-googleassistant');
const { Dialogflow } = require('jovo-platform-dialogflow');
const { JovoDebugger } = require('jovo-plugin-debugger');
const { Firestore } = require('jovo-db-firestore');

// ------------------------------------------------------------------
// APP INITIALIZATION
// ------------------------------------------------------------------

const app = new App();

// prettier-ignore
app.use(
  new GoogleAssistant(),
  new Dialogflow(),
  new JovoDebugger(),
  new Firestore(),  
);

// ------------------------------------------------------------------
// APP LOGIC
// ------------------------------------------------------------------


app.setHandler({
  LAUNCH() {
    return this.toIntent('HelloWorldIntent');
  },

  HelloWorldIntent() {
    this.ask("Hello World! What's your name?", 'Please tell me your name.');
  },

  MyNameIsIntent() {
    this.tell('Hey ' + this.$inputs.name.value + ', nice to meet you!');
  },
});

module.exports = { app };
