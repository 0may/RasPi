#include "ofApp.h"
#include "wiringPi.h"


ofApp::ofApp(string videoFilePath)
{
	this->videoFilePath = videoFilePath;
}


//--------------------------------------------------------------
void ofApp::setup()
{
	wiringPiSetup();
	pinMode(0, INPUT);
	pinState = 0;

	string videoPath = ofToDataPath(videoFilePath, true);

	ofxOMXPlayerSettings settings;
	settings.videoPath = videoPath;
	settings.useHDMIForAudio = true;
	settings.enableTexture = false;
	settings.enableLooping = true;
	settings.enableAudio = true;
	settings.listener = &omxlistener;

	omxPlayer.setup(settings);

	omxPlayer.setPaused(true);
	omxPlayer.setAlpha(0);
	omxPlayer.seekToFrame(0);

	ofHideCursor();
}


//--------------------------------------------------------------
void ofApp::update()
{
	if (digitalRead(0) != 0 && pinState == 0) {
//		cout << "pin high" << endl;
		pinState = 1;
		omxPlayer.setAlpha(255);
		omxPlayer.setPaused(false);
	}
	else if (digitalRead(0) == 0 && pinState == 1) {
//		cout << "pin low" << endl;
		pinState = 0;
	}
}


//--------------------------------------------------------------
void ofApp::draw(){
	ofBackground(0);
}


