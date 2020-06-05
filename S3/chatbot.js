
var chatHistory = [];
var apigClient = null;
// const AWS =require('aws-sdk');
var url_string = window.location.href;
// var cognito_token = url_string.substring(url_string.indexOf("=") + 1,url_string.indexOf("&"));

// AWS.config.region = 'us-east-1';
// AWS.config.credentials = new AWS.CognitoIdentityCredentials({
//   IdentityPoolId: 'Your Identity Pool ID',
// 	Logins: {
// 	   'cognito-idp.us-east-1.amazonaws.com/us-east-1_8MsV07uIJ': cognito_token
// 	}
// });

function callChatbotLambda() {
  var itext = document.getElementById('user-input-text').value.trim()
  var inputText = itext.toLowerCase();
  document.getElementById('user-input-text').value = "";
  if(inputText == "") {
    alert("Please enter some text");
    return false;
  }else {
    chatHistory.push("User: " + itext);
    document.getElementById('chat-output').innerHTML = "";
    chatHistory.forEach((element) => {
      document.getElementById('chat-output').innerHTML += "<p>" + element + "</p>";
    });
    setTimeout(chatbotResponse, 500, inputText);
    return false;
  }
}

// function chatbotResponse(inputText) {
//   // return AWS.config.credentials.getPromise()
//   // .then(()=>{
//   //   console.log('Successfully logged!');
//   apigClient = apigClientFactory.newClient({
//   //     accessKey: AWS.config.credentials.accessKeyId,
//   //     secretKey: AWS.config.credentials.secretAccessKey,
//   //     // sessionToken: AWS.config.credentials.sessionToken
//      });
//     var params = {};
//     var body = {
//       "message":inputText,
//       "userId":"lf0c"
//       // "identityID":AWS.config.credentials._identityId
//     };
//     var additionalParams = {
//       // headers: {
//       //   'x-api-key': 'Your API KEY'
//       // },
//       // queryParams: {}
//     };
//     console.log(body)
//     return apigClient.chatbotPost(params,body,additionalParams)
//   // })
//    .then((result) =>{
      
//       chatHistory.push("Bot: " + result.message);
//       document.getElementById('chat-output').innerHTML = "";
//       console.log(result.message)
//       chatHistory.forEach((element) => {
//         document.getElementById('chat-output').innerHTML += "<p>" + element + "</p>";
//       });
//   })
//   .catch((err) =>{
//     console.log(err);
//   });
//  }


function chatbotResponse(inputText) {
  // return AWS.config.credentials.getPromise()
  // .then(()=>{
  //   console.log('Successfully logged!');
  apigClient = apigClientFactory.newClient({
  //     accessKey: AWS.config.credentials.accessKeyId,
  //     secretKey: AWS.config.credentials.secretAccessKey,
  //     // sessionToken: AWS.config.credentials.sessionToken
     });
    var params = {};
    var body = {
      "message":inputText,
      "userId":"lf0c"
      // "identityID":AWS.config.credentials._identityId
    };
    var additionalParams = {
      // headers: {
      //   'x-api-key': 'Your API KEY'
      // },
      // queryParams: {}
    };
    console.log(body)
    return apigClient.chatbotPost(params,body,additionalParams)
  // })
   .then((result) =>{
    //  console.log(result)
      // response = result.data.body.message;
      // console.log(response);
      // message=JSON.stringify({result:[{message}]})
      //r=JSON.stringify(result);
      //var obj = JSON.parse(r);
      //r1 = obj["data"];
      r1 = result["data"];
      r2 = JSON.stringify(r1);
      r3 = r2.substring(3, r2.length-3);

      chatHistory.push("Bot: " + r3);
      document.getElementById('chat-output').innerHTML = "";
      // console.log(message)
      chatHistory.forEach((element) => {
        document.getElementById('chat-output').innerHTML += "<p>" + element + "</p>";
      });
  })
  .catch((err) =>{
    console.log(err);
  });
 }

//  function chatbotResponse(message) {
//   const delay = message.split(" ").length * 100;

//   fetch('https://4xthp0sc7a.execute-api.us-east-1.amazonaws.com/dev/chatbot', {
//     method: 'POST',
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({BotRequest:[{Message:message}]})
//   })
//   .then((res)=>{
//     res.json().then((responseObject)=>{
//       setTimeout(() => {
//         if(responseObject.body){
//           appendMessage(BOT_NAME, BOT_IMG, "left", responseObject.body);
//         } else {
//           appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
//         }
//       }, delay);
//     }).catch(()=>{
//       setTimeout(() => {
//         appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
//       }, delay);
//     })
//   })
//   .catch((a)=>{
//     setTimeout(() => {
//       appendMessage(BOT_NAME, BOT_IMG, "left", "I don't understand that!");
//     }, delay);
//   })

// }