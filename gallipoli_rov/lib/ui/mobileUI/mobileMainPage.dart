import 'package:control_pad/control_pad.dart';
import 'package:control_pad/models/pad_button_item.dart';
import 'package:control_pad/views/joystick_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:gallipoli_rov/ui/mobileUI/display/mobileDisplayLandSpace.dart';
import 'package:web_socket_channel/io.dart';

class MobileMainPage extends StatefulWidget {

  String urlAdress;
  IOWebSocketChannel webSocketChannel;


  MobileMainPage({Key key,this.webSocketChannel,this.urlAdress}) : super(key: key);

  @override
  _MobileMainPageState createState() => _MobileMainPageState();
}

class _MobileMainPageState extends State<MobileMainPage> {

  var ip_adress=TextEditingController();
  var ip_adress_port=TextEditingController();

  bool login=false;

  @override
  void initState() {
    // TODO: implement initState
    
    SystemChrome.setEnabledSystemUIOverlays([SystemUiOverlay.bottom]);
  
    super.initState();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
        appBar: AppBar(
            title: Text("GALLİPOLU ROV 2020 TEKNOFEST"),
          ),
          body: pageMain(),
        floatingActionButton: FloatingActionButton(
          onPressed: (){
            return Navigator.push(
              context, 
             MaterialPageRoute(builder: (context)=>MobileDisplayLandSpace(ip_adress: ip_adress.text.toString(),ip_adress_port: ip_adress_port.text.toString(),))
            );
        },
        child: Icon(Icons.send),
       ),
     );
  }

  Widget pageMain(){

    return Center(
      child: Column(
        children: [
          FlutterLogo(),
          TextField(
            controller:  ip_adress,
            decoration: InputDecoration(
              labelText: "ROV IP Adres giriniz.",
              hintText: "ROV IP Adres giriniz.",
              border: OutlineInputBorder()
            ),
          ),
          Divider(color: Colors.blue,height: 15,),
          TextField(
            controller:  ip_adress_port,
            decoration: InputDecoration(
              labelText: "ROV IP Adres PORT çıkışı giriniz.",
              hintText: "ROV IP Adres PORT çıkışı giriniz.",
              border: OutlineInputBorder()
            ),
          ),
        ],
      ),
    );
  }
}