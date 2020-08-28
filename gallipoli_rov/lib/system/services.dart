import 'package:flutter/cupertino.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class ServicesSendWebsockets extends ChangeNotifier {

  WebSocketChannel channel;
  String host;
  String port;
  dynamic _data;

  ServicesSendWebsockets({this.channel});

  WebSocketChannel connection({String clientHost,String clientPort}){

    channel =IOWebSocketChannel.connect('ws://$clientHost:$clientPort');

    return channel;
  }
  

  String sendData(String data,{String clientHost,String clientPort}){

    // if((host==null) || hostF!=null ){
      
    //   if(host!=null){
    //     hostF=host;
    //   }
    // }
    
    channel=connection(clientHost: clientHost,clientPort: clientPort);
    if(data!=null){
      channel.sink.add(data);
      channel.stream.listen((dataStream){
        _data=dataStream;
        notifyListeners();
        // print(dataStream);
      });
    }
    else{
      print("Data null");
    }

  }

    dynamic get getData => _data;


}