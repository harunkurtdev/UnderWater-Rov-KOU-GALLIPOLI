import 'package:flutter/material.dart';
import 'package:gallipoli_rov/system/services.dart';
import 'package:gallipoli_rov/ui/mainPage.dart';
import 'package:provider/provider.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (context)=>ServicesSendWebsockets()),
        ],
          child: MaterialApp(
          title: 'Flutter Demo',
          theme: ThemeData(
            primarySwatch: Colors.blue,
          ),
          home:MainPage() ,
        ),
    );
  }
}
