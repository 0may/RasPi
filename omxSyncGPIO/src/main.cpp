#include "ofMain.h"
#include "ofApp.h"

int main(int argc, char** argv)
{
	if (argc != 2) {
		cerr << "Error: Please specify the file path to a single video file." << endl;
		return 1;
	}
	else {
		cout << "Run with video file '" << argv[1] << "'" << endl;
	}

	ofSetLogLevel(OF_LOG_SILENT);
	ofSetupOpenGL(1280, 720, OF_FULLSCREEN);

	ofApp* app = new ofApp(string(argv[1]));
	ofRunApp(app);
}
