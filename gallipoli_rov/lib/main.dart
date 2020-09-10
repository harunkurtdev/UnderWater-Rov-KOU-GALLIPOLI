import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:gallipoli_rov/system/websocket_Client/servicesSendWebsockets.dart';
import 'package:gallipoli_rov/ui/mainPage.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (context)=>ServicesSendWebsockets())
        ],
        child: MaterialApp(
        title: 'GalliPoli Rov 2020',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.blue,
        //  visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        initialRoute: "/",
        routes: {
          "/":(context)=>MainPage(),
        },
      ),
    );
  }
}

