import 'dart:typed_data';

import 'package:control_pad/control_pad.dart';
import "package:flutter/material.dart";
import 'package:gallipoli_rov/system/services.dart';
import 'package:provider/provider.dart';

import 'dart:convert';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  static WebSocketChannel channel;
   TextEditingController sendDataController,clientHostController,clientPortController;
  final List<String> list = [];
  static ServicesSendWebsockets sendWebsockets;
  
  static String images = "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";
  static  Uint8List bytes = base64.decode(images);

  @override
  void initState() {
    super.initState();
    //channel = IOWebSocketChannel.connect('ws://172.19.96.191:65432');
    //controller = TextEditingController();
    sendDataController = TextEditingController();
    clientHostController = TextEditingController();
    clientPortController = TextEditingController();
    //channel.stream.listen((data) => setState(() => list.add(data)));
    sendWebsockets= ServicesSendWebsockets(channel: channel);
    channel=sendWebsockets.connection(clientHost:"192.168.1.7",clientPort: "5001");
  }



  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ServicesSendWebsockets>(
          builder: (BuildContext context, value, Widget child) { 
             
             value.sendData("data",clientHost:"192.168.1.5",clientPort: "5001");
             
             bytes = base64.decode(ascii.decode(value.getData));

              return Scaffold(
        appBar: AppBar(
          title: Text('GalliPoli Rov TeknoFest 2020'),
        ),
        body: SingleChildScrollView(
                child: Container(
            padding: EdgeInsets.all(20.0),
            child: Column(
              children: <Widget>[
                Form(
                  child: Column(                
                    children: <Widget>[
                      TextFormField(
                    controller: sendDataController,
                    decoration: InputDecoration(
                      labelText: "Send Data",
                    ),
                  ),
                    TextFormField(
                    controller: clientHostController,
                    decoration: InputDecoration(
                      labelText: "ClientHost",
                    ),
                  ),
                    TextFormField(
                    controller: clientPortController,
                    decoration: InputDecoration(
                      labelText: "ClientPort",
                    ),
                  ),
                    ],
                  )
                ),
                Center(
                  child: FloatingActionButton(onPressed: (){
                    
                    channel=sendWebsockets.connection(clientHost:"192.168.1.5",clientPort: "5001");
                    channel.sink.add("denmee");
                    channel.stream.listen((data){
                      setState(() {
                        print(data);
                        bytes = base64.decode(ascii.decode(data));
                      });
                    });
                    
                  }),
                ),
                Center(
                  child: Container(
                    width: 200,
                    height: 200,
                    child:Image.memory(bytes,
                    gaplessPlayback: true,
                    )
                  ),
                ),
                Column(
                  children: list.map((data) => Text(data)).toList(),
                ),
                Container(
                  child: JoystickView(
                    size: 100,
                    onDirectionChanged: (x,y){
                      sendWebsockets.sendData(y.toString(),clientHost:"192.168.1.5",clientPort: "65432");
                    },
                  ),
                ),


                // StreamBuilder(
                //   stream: periodicStream,
                //   builder: (BuildContext context, AsyncSnapshot snapshot) {

                //     switch (snapshot.connectionState) {
                      
                //       case ConnectionState.none:
                //         // TODO: Handle this case.
                //         return Text("data");
                //         break;
                //       case ConnectionState.waiting:
                //         // TODO: Handle this case.

                //         return Text("Data");
                //         break;
                //       case ConnectionState.active:
                //         // TODO: Handle this case.
                        
                //         return Text("Data");
                //         break;
                //       case ConnectionState.done:
                //         // TODO: Handle this case.
                        
                //         return Text("Data");
                //         break;
                //     }
                    
                //   },
                // ),
              ],
            ),
          ),
        ),
        floatingActionButton: FloatingActionButton(
          child: Icon(Icons.send),
          onPressed: () {
              // sendData();
              print(clientPortController.text.toString() +" "+clientHostController.text.toString());
              String data=sendWebsockets.sendData(sendDataController.text.toString(),clientHost:"192.168.1.5",clientPort: "65432");
              // print(data);        
            
            // channel.sink.close();
            // setState(() {
            // channel = IOWebSocketChannel.connect('ws://172.19.96.191:65432');        
            // });
          },
        ),
      );


           },
          child: Container(),
    );
  }
}