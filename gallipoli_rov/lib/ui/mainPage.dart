import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:gallipoli_rov/ui/desktopUI/dektopMainPage.dart';
import 'package:gallipoli_rov/ui/mobileUI/mobileMainPage.dart';
import 'package:gallipoli_rov/ui/webUI/webMainPage.dart';

class MainPage extends StatefulWidget {
  MainPage({Key key}) : super(key: key);

  @override
  _MainPageState createState() => _MainPageState();
}


class _MainPageState extends State<MainPage> {
    
    
    @override
  void initState() {
    // TODO: implement initState
    super.initState();

  }
  
      

  @override
  Widget build(BuildContext context) {

      /*showDialog(
        context: context,
        builder: (context){
            return Container(
                child: Center(
                  child: Column(
                    children: [
                      TextField(
                        decoration: InputDecoration(
                          hintText: "Lütfen Bağlantı adresini seçiniz..."
                        ),
                      )
                    ],
                  )
                ),  
            );
          }
        );*/

      if(Platform.isAndroid || Platform.isIOS){
        //mobil ise
        return MobileMainPage();
      }
      else if (Platform.isWindows || Platform.isMacOS || Platform.isLinux){
        // masaüstü ise
        return DesktopMainPage();
      }
      else {
        // web ise
        return WebMainPage();
      }

  }
}
