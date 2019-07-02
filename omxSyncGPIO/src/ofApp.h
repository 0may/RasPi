#pragma once

#include "ofMain.h"
#include "ofxOMXPlayer.h"

class OMXPlayerListener : public ofxOMXPlayerListener {
	void onVideoEnd(ofxOMXPlayer* player) {
		cout << "vid end" << endl;
		player->start();
		player->setPaused(true);
		player->seekToFrame(0);
	}

	void onVideoLoop(ofxOMXPlayer* player) {
		cout << "loop end" << endl;
		player->setAlpha(0);
		player->setPaused(true);
		player->seekToFrame(0);
	}
};


class ofApp : public ofBaseApp{

	public:
		ofApp(string videoFilePath);
		void setup();
		void update();
		void draw();

	protected:
		ofxOMXPlayer omxPlayer;
		OMXPlayerListener omxlistener;
		int pinState;
		string videoFilePath;

};

