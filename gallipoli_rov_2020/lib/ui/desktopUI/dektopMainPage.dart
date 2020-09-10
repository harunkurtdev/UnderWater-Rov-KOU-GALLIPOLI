import 'package:flutter/material.dart';
import 'package:gallipoli_rov_2020/ui/mobileUI/display/mobileDisplayLandSpace.dart';
import 'package:web_socket_channel/io.dart';

class DesktopMainPage extends StatefulWidget {

  DesktopMainPage({Key key}) : super(key: key);

  @override
  _DesktopMainPageState createState() => _DesktopMainPageState();
}

class _DesktopMainPageState extends State<DesktopMainPage> {
  

  void none(){

  }

  void waiting(){

  }

  void done(){

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
          /*appBar: AppBar(
            //title: Text("GALLİPOLU ROV 2020 TEKNOFEST"),
          ),*/
          body: StreamBuilder<Object>(
            stream: null,
            builder: (context, snapshot) {
              return OrientationBuilder(
                  builder: (BuildContext context, Orientation orientation) { 
                    //burada ekran dikeyde ise diyoruz
                    if(orientation==Orientation.portrait){
                        ///ekran dik ise aşağı daki stream dan gelen
                        ///bilgileri üzerine inşa edilsin

                        switch(snapshot.connectionState){

                          case ConnectionState.none:
                            // TODO: Handle this case.
                            return Container(
                              child: Text("Dikey de"),
                            );
                            break;
                          case ConnectionState.waiting:
                            // TODO: Handle this case.
                            break;
                          case ConnectionState.active:
                            // TODO: Handle this case.
                            break;
                          case ConnectionState.done:
                            // TODO: Handle this case.
                            break;
                        }

                    }else{
                       
                       switch(snapshot.connectionState){

                          case ConnectionState.none:
                            // TODO: Handle this case.
                            return MobileDisplayLandSpace();
                            break;
                          case ConnectionState.waiting:
                            // TODO: Handle this case.
                            break;
                          case ConnectionState.active:
                            // TODO: Handle this case.
                            break;
                          case ConnectionState.done:
                            // TODO: Handle this case.
                            break;
                        }
                    
                    }
                  },
                ); 
              }
          ),
    );
  }
}