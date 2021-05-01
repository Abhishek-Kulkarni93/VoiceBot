'use strict';

const { App } = require('jovo-framework');
const { Alexa } = require('jovo-platform-alexa');
const { GoogleAssistant,
        BasicCard,
        Carousel,
        List,
        OptionItem,
        CarouselBrowse,
        CarouselItem,
        CarouselBrowseTile,
        Table } = require('jovo-platform-googleassistant');
const { JovoDebugger } = require('jovo-plugin-debugger');
const { FileDb } = require('jovo-db-filedb');
const { Dialogflow } = require('jovo-platform-dialogflow');
const {Firestore} = require('jovo-db-firestore');


// ------------------------------------------------------------------
// APP INITIALIZATION
// ------------------------------------------------------------------

const app = new App();
const admin = require('firebase-admin');

// const serviceAccount = require('./secrets/digengproject01-firebase-adminsdk-ci8o7-5dd170bf3e.json');

admin.initializeApp();

// UNCOMMENT THIS TO RUN ON LOCAL MACHINE
// admin.initializeApp({
//   credential: admin.credential.applicationDefault(),
//   databaseURL: 'https://digengproject01.firebaseio.com'
// });

const db = admin.firestore();

app.use(
  new Dialogflow(),
  new Alexa(),
  new GoogleAssistant(),
  new JovoDebugger(),
  new FileDb(),
  new Firestore({}, db)
);


// ------------------------------------------------------------------
// APP LOGIC
// ------------------------------------------------------------------

app.setHandler({
  LAUNCH() {
    return this.toIntent('HelloWorldIntent');
  },

/*   HelloWorldIntent() {
    // this.ask("Hello World! What's your name?", 'Please tell me your name.');
    this.$googleAction.askForConfirmation("Hey there! Please choose FIN or FEIT department");
  }, */

  HelloWorldIntent() {
    const list = new List();
    list.setTitle('Examination Departments');

    list.addItem(
        (new OptionItem())
            .setTitle('FIN')
            .setDescription('FIN Exam Department')
            .setKey('fin')
    );
    list.addItem(
        (new OptionItem())
        .setTitle('FEIT')
        .setDescription('FEIT Exam Department')
        .setKey('feit')
    );

    this.$googleAction.showList(list);
    // this.$googleAction.showSuggestionChips(['FIN', 'FEIT']);
    let deptMsg = "Select your department";
    if(this.$session.$data.customDeptMsg) {
      deptMsg = this.$session.$data.customDeptMsg;
    }
    this.ask(deptMsg, 'Choose your department');
},

async FinDeptIntent() {
  this.$session.$data.dept = "fin";
  const deptRef = db.collection('dept').doc(this.$session.$data.dept);
    const doc = await deptRef.get();
    this.$session.$data.deptData = doc.data()
  this.ask(`You have selected ${this.$session.$data.deptData['name']}. How can I help you?`, 
  `You have selected ${this.$session.$data.dept.toUpperCase()}. What information do you need?`);
},

async FeitDeptIntent() {
  this.$session.$data.dept = "feit";
  const deptRef = db.collection('dept').doc(this.$session.$data.dept);
    const doc = await deptRef.get();
    this.$session.$data.deptData = doc.data()
  this.ask(`You have selected ${this.$session.$data.deptData['name']}. How can I help you?`, 
  `You have selected ${this.$session.$data.dept.toUpperCase()}. What information do you need?`);
},

ContactInfoIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }

  // const deptInfo = require('./contact_info')[this.$session.$data.dept];
  const deptInfo = this.$session.$data.deptData
  const responseString = `
  ${this.$session.$data.deptData['name']} Department
  Email: ${deptInfo["Email ID"]}
  Phone: ${deptInfo["Tel No"]}
  Fax: ${deptInfo["Fax No"]}
  Address: ${deptInfo["Address"]}

  Do you need more information?
  `;

  this.ask(responseString);

},

ContactEmailIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }

  // const deptInfo = require('./contact_info')[this.$session.$data.dept];
  const deptInfo = this.$session.$data.deptData
  this.ask(`${this.$session.$data.deptData['name']} Department's Email id is ${deptInfo["Email ID"]}`)
},

ContactPhoneIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }
  const dept = this.$session.$data.dept

  // const deptInfo = require('./contact_info')[this.$session.$data.dept];
  const deptInfo = this.$session.$data.deptData
  if(dept === "fin") {
  this.ask(`${this.$session.$data.deptData['name']} Department's Phone number is ${deptInfo["Tel No"]}`)
  }
  else{
  this.ask(`${this.$session.$data.deptData['name']} Department's Phone number is ${deptInfo["Tel no."]}`)
  }
},

ContactAddressIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }
  // const deptInfo = require('./contact_info')[this.$session.$data.dept];
  const deptInfo = this.$session.$data.deptData
  this.ask(`${this.$session.$data.deptData['name']} Department's Address is ${deptInfo["Address"]}. Do you need more information?`)
},

ContactFaxIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }
  const deptInfo = this.$session.$data.deptData
  if(dept === "fin") {
    this.ask(`${this.$session.$data.deptData['name']} Department's FAX is ${deptInfo["Fax No"]}`)
  }
  else{
    this.ask(`${this.$session.$data.deptData['name']} Department's FAX is ${deptInfo["Fax no."]}`)
  }
  // const deptInfo = require('./contact_info')[this.$session.$data.dept];
},

DeptInfoIntent() {
  const dept = this.$session.$data.dept
  const deptInfo = this.$session.$data.deptData
  if(dept === "fin") {
    this.ask(`Here are the Exam office hours for ${dept}.  
                Monday: ${deptInfo["Monday"]},
                Tuesday: ${deptInfo["Tuesday"]} and
                Wednesday: ${deptInfo["Wednesday"]}.
                Do you need more information?`);
  }
  else {
    this.ask(`Please contact the Examination Office by telephone or Email. Personal appointments are possible for exceptional cases. Alternatively, you can visit the following link for current updates: ${deptInfo["Personal Consultation"]}. Do you need more information?`);
  }
},

DeptOpenIntent() {
  const deptInfo = this.$session.$data.deptData
  const weekday = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"
  };
  const day = weekday[new Date(this.$inputs["date-time"].key).getDay()];

  if (['Monday','Tuesday','Wednesday'].indexOf(day) === -1) {
    this.ask(`Office is not open on ${day}. Do you need more information?`);
  } else {
    this.ask(`Yes, the Exam office is open on ${day}. Here are the timings: ${deptInfo[day]}. Do you need more information?`);
  }
},

DeptCloseIntent() {
  const deptInfo = this.$session.$data.deptData
  const weekday = {
    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"
  };
  const day = weekday[new Date(this.$inputs["date-time"].key).getDay()];

  if (['Monday','Tuesday','Wednesday'].indexOf(day) > -1) {
    this.ask(`No, the Exam office is open on ${day}. The timings are: ${deptInfo[day]}. Do you need more information?`);
  } else {
    this.ask(`Yes, it is closed on ${day}. Do you need more information?`);
  }
},

MoreInfoYesIntent() {
  const list = new List();
    list.setTitle('More information on');

    list.addItem(
        (new OptionItem())
            .setTitle('Email ID')
            .setDescription('')
            .setKey('emailid')
    );
    list.addItem(
        (new OptionItem())
        .setTitle('Phone Number')
        .setDescription('')
        .setKey('phonenumber')
    );
    list.addItem(
      (new OptionItem())
      .setTitle('Address')
      .setDescription('')
      .setKey('address')
  );

    this.$googleAction.showList(list);
  this.ask('What information do you need?') 
},

ExamResultInfoIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`The results can be found on your LSF portal. After logging in with your student credentials, click on the 'Administration of Exams' tab and then choose 'Transcript of records'. Here's the link: ${deptInfo['result_link']}. Do you need more information?`);
},

ConsultationIntent() {
  const dept = this.$session.$data.dept
  const deptInfo = this.$session.$data.deptData
  if(dept === "fin") {
    this.ask(`${deptInfo["Personal consultation"]}. Do you need more information?`)
  }
  else{
    this.ask(`${deptInfo["Office Hour"]}. For current updates, visit the following link: ${deptInfo["Personal consultation"]}. Do you need more information?`)
  }
},

ExamRegistrationIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`Go to the following link:${deptInfo["Examination Plans"]} and you will find the required information. Alternatively, you can login to the LSF portal and click on Administration of Exams and then click on Apply for exams.`)
},

ExamInfoIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`Go to the following link:${deptInfo["Examination Plans"]} to find the exam info. Alternatively, you can login to the LSF portal and click on Administration of Exams and then click on Info on exams.`)
},

ExamBoardIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`Go to the following link:${deptInfo["Examination Board"]} to find the required information.`)
},

ExamFormsIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`Go to the following link:${deptInfo["Forms"]} to find the required information.`)
},

ExamDeadlineIntent() {
  const dept = this.$session.$data.dept
  const deptInfo = this.$session.$data.deptData
  if(dept === "fin") {
    this.ask(`Go to the following link:${deptInfo["Deadlines"]} to find the required information.`)
  }
  else{
    return this.toIntent('Default Fallback Intent')
  }
},

ModulesInfoIntent() {
  const deptInfo = this.$session.$data.deptData
  this.ask(`Go to the following link:${deptInfo["Study Regulations"]} to find the required information.`)
},

DeregistrationInfoIntent() {
  this.ask(`Login to the LSF portal and click on Administration of Exams and then click on Apply for exams to find the deregister option. Alternatively, you can mail the examination office.`)
},

DefaultFallBackIntent() {
  this.ask(`Sorry! I don't know that. You can contact the Examination office to know more. Would you like to know anything else?`)
},


async DeptChangeIntent() {
  if(!this.$session.$data.dept) {
    this.$session.$data.customDeptMsg = "Please select your department first.";
    return this.toIntent('HelloWorldIntent');
  }
  const currentDept = this.$session.$data.dept;
  this.$session.$data.dept = (this.$session.$data.dept === "fin") ? "feit" : "fin";
  const deptRef = db.collection('dept').doc(this.$session.$data.dept);
    const doc = await deptRef.get();
    this.$session.$data.deptData = doc.data()
  this.ask(`You have switched from ${currentDept.toUpperCase()} to ${this.$session.$data.dept.toUpperCase()} department. What information do you need?`)
},

MoreInfoNoIntent() {
  this.tell('Thank you for using our bot, hope it was helpful! Have a nice day!') 
},

async ON_ELEMENT_SELECTED() {
  // this.tell(this.getSelectedElementId() + ' selected');
  if (["fin","feit"].indexOf(this.getSelectedElementId()) > -1) {
    this.$session.$data.dept = this.getSelectedElementId();
    const deptRef = db.collection('dept').doc(this.$session.$data.dept);
    const doc = await deptRef.get();
    this.$session.$data.deptData = doc.data()
  } else {
    this.$session.$data.info = this.getSelectedElementId();
  }
  
  if (!this.$session.$data.info) {
    this.ask(`You have selected ${this.$session.$data.deptData['name']}. How can I help you?`, 
  `You have selected ${this.$session.$data.deptData['name']}. What information do you need?`);
  } else {
    // const deptInfo = require('./contact_info')[this.$session.$data.dept];
    const deptInfo = this.$session.$data.deptData
    this.ask(`${this.$session.$data.deptData['name']}'s ${this.$session.$data.info} is ${deptInfo[this.$session.$data.info]}. Do you need any other information?`);
  }
  
},

});

module.exports = { app };
