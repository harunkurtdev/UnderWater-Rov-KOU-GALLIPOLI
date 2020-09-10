import 'dart:typed_data';

import 'package:control_pad/control_pad.dart';
import 'package:control_pad/models/gestures.dart';
import 'package:control_pad/models/pad_button_item.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:gallipoli_rov/system/websocket_Client/servicesSendWebsockets.dart';
import 'package:provider/provider.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';

class MobileDisplayLandSpace extends StatefulWidget {

  String ip_adress;
  String ip_adress_port;

  MobileDisplayLandSpace({Key key,this.ip_adress,this.ip_adress_port}) : super(key: key);

  @override
  _DisplayLandSpaceState createState() => _DisplayLandSpaceState();
}

class _DisplayLandSpaceState extends State<MobileDisplayLandSpace> {
  String ip;
  String port;
  Uint8List bytes;
 ServicesSendWebsockets sendWebsockets;
 WebSocketChannel channel;

  @override
  void initState() {
    // TODO: implement initState
    ip = widget.ip_adress;
    port=widget.ip_adress_port;
    sendWebsockets=ServicesSendWebsockets(channel: channel);
    channel=sendWebsockets.connection(clientHost: ip,clientPort: port);
    SystemChrome.setEnabledSystemUIOverlays([SystemUiOverlay.bottom]);
    
    super.initState();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    channel.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ServicesSendWebsockets>(
      builder: (BuildContext context, ServicesSendWebsockets value, Widget child) { 
        
        value.sendData("mobile",clientHost: ip.toString(),clientPort: port.toString());

          if(value. getData!=null){
            bytes=base64.decode(ascii.decode(value.getData));

            return Container(
                    child: Stack(
                      children: [
                        Container(
                        color:Colors.blue,
                        child: Stack(
                          children: [
                            Container(
                              width: double.infinity,
                              height: double.infinity,
                              child: Image.memory(bytes,
                              gaplessPlayback: true,
                              fit: BoxFit.cover,
                              ),
                            ),
                            Align(
                              alignment: Alignment.topCenter,
                              child: Container(
                                width: 100,
                                height: 100,
                                child: Image.memory(bytes,
                              gaplessPlayback: true,
                                fit: BoxFit.fitHeight,
                                ),
                              ),
                            ),
                            Align(
                              alignment: Alignment.topRight,
                              child: Container(
                                width: 100,
                                height: 100,
                                child: Image.memory(bytes,
                              gaplessPlayback: true,
                                fit: BoxFit.contain,
                                ),
                              ),
                            )
                          ],
                        )
                        ),
                        Positioned(
                          left: 200,
                          bottom: 25,
                          child: RotatedBox(
                            quarterTurns: 1,
                            child: Container(
                                child: PadButtonsView(
                                buttons: [
                                  PadButtonItem(index: 1,buttonText: "-"),
                                  PadButtonItem(index: 2,buttonText: "+"),
                                ],
                                size: 200,
                              ),
                              ),
                          ),
                          ),
                        Positioned(
                          left: 25,
                          bottom: 25,
                          child: Container(
                              child: JoystickView(
                                backgroundColor: Colors.transparent,
                                size: 200,
                                onDirectionChanged: (x,y){
                                  //print("X ekseni : "+x.toString()+" --- "+"Y ekseni : "+ y.toString());
                                  
                                  sendWebsockets.sendData(x.toString(),clientHost: ip,clientPort: port); 
                                  
                                },
                              ),
                            ),
                          ),
                          Positioned(
                          right: 25,
                          bottom: 25,
                          child: Container(
                              child: PadButtonsView(
                                buttons: [
                                  PadButtonItem(index: 1,buttonText: "+"),
                                  PadButtonItem(index: 2,buttonText: "-"),
                                  PadButtonItem(index: 3,buttonText: "A"),
                                  PadButtonItem(index: 4,buttonText: "B"),
                                  PadButtonItem(index: 5,buttonText: "C"),
                                ],
                                size: 200,
                                padButtonPressedCallback: (index,detector){
                                  switch (detector) {
                                    case Gestures.TAPDOWN:
                                      // TODO: Handle this case.
                                        print(index);
                                        
                                  sendWebsockets.sendData("merhaba",clientHost: ip,clientPort: port); 
                                      break;
                                    case Gestures.TAPUP:
                                      // TODO: Handle this case.
                                      break;
                                    case Gestures.TAPCANCEL:
                                      // TODO: Handle this case.
                                      break;
                                    case Gestures.TAP:
                                      // TODO: Handle this case.
                                      break;
                                    case Gestures.LONGPRESS:
                                      // TODO: Handle this case.
                                      break;
                                    case Gestures.LONGPRESSSTART:
                                      // TODO: Handle this case.
                                      break;
                                    case Gestures.LONGPRESSUP:
                                      // TODO: Handle this case.
                                      break;
                                  }
                                },
                              ),
                            ),
                          ),
                      ],
                    ),
                  );

              }else{
                return Container(
                  child: Center(
                        child: Column(
                          children: [
                            Text("DATA Gelmiyor... Lütfen Bağlantıları Kontrol Ediniz."),
                            CircularProgressIndicator()
                          ],
                        ),
                  ),
                );
              }
         },
      );
  }
}