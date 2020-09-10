import 'package:flutter/material.dart';

class WebMainPage extends StatefulWidget {
  WebMainPage({Key key}) : super(key: key);

  @override
  _WebMainPageState createState() => _WebMainPageState();
}

class _WebMainPageState extends State<WebMainPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
          body: Container(
         child: Center(
           child: Text("Web"),
         )
      ),
    );
  }
}