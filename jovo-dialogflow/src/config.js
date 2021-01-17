// ------------------------------------------------------------------
// APP CONFIGURATION
// ------------------------------------------------------------------

module.exports = {
  logging: true,

  intentMap: {
    'AMAZON.StopIntent': 'END',
  },

  db: {
    FileDb: {
      pathToFile: '../db/db.json',
    },
    Firestore: {
      credential: require('./secrets/digengproject01-firebase-adminsdk-ci8o7-5dd170bf3e.json'),
      databaseURL: 'https://digengproject01.firebaseio.com',
      collectionName: 'dept'
  }
  },
};
