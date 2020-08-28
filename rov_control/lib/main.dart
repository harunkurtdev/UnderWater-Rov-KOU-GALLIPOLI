import 'dart:async';

import 'package:flame_gamepad/flame_gamepad.dart';
import "package:flutter/material.dart";
// import 'package:flutter_vlc_player/vlc_player.dart';
// import 'package:flutter_vlc_player/vlc_player_controller.dart';
import 'package:webview_flutter/webview_flutter.dart';

class MainLayout extends StatefulWidget {

  @override
  _MainLayoutState createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  String url="10.0.2.2:9875/video_feed";

  String video_feed="http://192.168.1.6:9875/video_feed";

  String denemeUrl="http://213.226.254.135:91/mjpg/video.mjpg";

  bool _isConnected = false;
  String _lastEvent = 'None';

  @override
  void initState() {
    super.initState();
    initPlatformState();

    FlameGamepad()
      ..setListener((String evtType, String key) {
        setState(() {
          if(evtType==GAMEPAD_BUTTON_A){
            _lastEvent = evtType + " " + key;
          }
          
        });
      });

      
  }

    Future<bool> checkIsConnected() async {
    return await FlameGamepad.isGamepadConnected;
  }

  Future<void> initPlatformState() async {
    bool isConnected;
    try {
      isConnected = await checkIsConnected();
    }catch (PlatformException) {
      isConnected = false;
    }

    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    if (!mounted) return;

    setState(() {
      _isConnected = isConnected;
    });
  }

  bool setts=true;
  // VlcPlayerController controller =new VlcPlayerController();
  Completer<WebViewController> _completer=Completer<WebViewController>();
  Stream stream=Stream.periodic(Duration(seconds: 2),(value)=>value);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        child: Text("pulse"),
        onPressed: (){
          setState(() {
            setts==true?true:false;
          });
        },
      ),
      body: StreamBuilder<Object>(
        stream: stream,
        builder: (context, snapshot) {
          return Column(
            children: <Widget>[
              // Expanded(
              //             child: Center(
              //     child: VlcPlayer(
              //       defaultHeight: 640,
              //        defaultWidth: 360,
              //         url: video_feed,
              //          controller: controller,
              //          placeholder:  Container(
              //               height: 250.0,
              //               child: Row(
              //                 mainAxisAlignment: MainAxisAlignment.center,
              //                 children: <Widget>[CircularProgressIndicator()],
              //               ),
              //             ),
              //          ),
              //   ),
              // ),
              Text('Is connected on: $_isConnected\n'),
              Text(_lastEvent),
              RaisedButton(
                  child: Text("Try connection again"),
                  onPressed: () async {
                    final isConnected = await checkIsConnected();
                    setState(() {
                      _isConnected = isConnected;
                    });
                  }
              ),
                   Expanded(
                        child: Center(
                       child: Container(
                         height: 3000,
                         width: 300,
                         child: WebView(
                           javascriptMode: JavascriptMode.unrestricted,
                           initialUrl: video_feed,
                           onWebViewCreated: (WebViewController webViewController){
                             _completer.complete(webViewController);
                           },
                         ),
                       ),
                     ),
                   ),
            ],
          );
        }
      ),
    );
  }
}

//"10.0.2.2:9875/video_feed"