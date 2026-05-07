import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {

apiKey:"AIzaSyBa4QKWUG9pAq0u5zNTHf1LZIKO8Ne42SM",

authDomain:"proyecto01-7b3d9.firebaseapp.com",

projectId:"proyecto01-7b3d9",

storageBucket:"proyecto01-7b3d9.firebasestorage.app",

messagingSenderId:"758629058015",

appId:"1:758629058015:web:1f921f9c74dd497b60b06a"

};

const app = initializeApp(
firebaseConfig
)

export const auth = getAuth(app)