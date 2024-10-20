// in bash
//npm install react-native-maps react-native-geolocation-service

//request permission for local access
import { PermissionsAndroid } from 'react-native';

async function requestLocationPermission() {
  try {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: "Location Access Permission",
        message: "App needs access to your location to provide safe walking paths",
        buttonNeutral: "Ask Me Later",
        buttonNegative: "Cancel",
        buttonPositive: "OK"
      }
    );
    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      console.log("You can access location");
    } else {
      console.log("Location permission denied");
    }
  } catch (err) {
    console.warn(err);
  }
}

// Track the user’s real-time location:
import Geolocation from 'react-native-geolocation-service';

Geolocation.getCurrentPosition(
  (position) => {
    console.log(position);
    // Send this data to your Python API for real-time zone checking
  },
  (error) => {
    console.log(error.code, error.message);
  },
  { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
);


////////////////////////////////////////////////////////////////////////
//Implement Real-time Processing (Edge AI Model)
//Install TensorFlow Lite and dependencies:
// in bash
// npm install @tensorflow/tfjs-react-native

//Load the pre-trained TensorFlow Lite model in React Native:
import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-react-native';

async function loadModel() {
  await tf.ready();
  const model = await tf.loadGraphModel('path_to_your_model/model.json');
  return model;
}

async function predictSafety(locationData) {
  const model = await loadModel();
  const inputTensor = tf.tensor([locationData]);
  const prediction = model.predict(inputTensor);
  console.log(prediction);
  // Based on prediction, trigger a notification or SOS alert
}


//You can use your Python API to return more data or trigger actions by calling it from the mobile app:
async function checkSafeZone(locationData) {
  const response = await fetch('https://your-api-endpoint/check-safe-zone', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(locationData)
  });
  const result = await response.json();
  return result;
}
///////////////////////////////////////////////////////////////////////////////////////////

//SOS Alert Mechanism
//Add a button in your mobile app’s UI to manually trigger SOS alerts.
<Button
  title="Send SOS"
  onPress={() => {
    // Call API or trigger a local notification
    triggerSOSAlert();
  }}
/>

//////EXAMPLE
//Automated Alerts:
//in bash
// npm install @react-native-community/push-notification-ios

import PushNotification from 'react-native-push-notification';

function sendNotification() {
  PushNotification.localNotification({
    title: "Warning",
    message: "You are entering an unsafe area!",
  });
}

function triggerSOSAlert() {
  PushNotification.localNotification({
    title: "SOS Alert",
    message: "Emergency! Sending your location to emergency contacts...",
  });
  // Also call your Python API to notify emergency services
}
