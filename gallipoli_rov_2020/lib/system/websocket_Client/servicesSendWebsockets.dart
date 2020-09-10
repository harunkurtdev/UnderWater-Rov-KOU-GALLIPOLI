

import 'package:flutter/widgets.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class ServicesSendWebsockets extends ChangeNotifier {

WebSocketChannel channel;
String _clientHost;
String _ClientPort;
dynamic _data;

  ServicesSendWebsockets({this.channel});

    WebSocketChannel connection({String clientHost,String clientPort}){
    channel=IOWebSocketChannel.connect("ws://$clientHost:$clientPort");
    return channel;

  }

  String sendData (String data,{String clientHost,String clientPort}){


    channel=connection(clientHost: clientHost,clientPort: clientPort);

    if(data!=null){
      channel.sink.add(data);
      channel.stream.listen((event) { 
        _data=event;
        notifyListeners();
      });
    }else{
      print("Data Null");
    }
  }

  dynamic get getData=>_data;

}