
import 'dart:io';

main()  {

  HttpServer.bind("6ce78d53-389b-459e-86eb-f3395e404572.local", 80).then((HttpServer server){

    print("weboscket hzır");

    server.listen((HttpRequest request){

      HttpResponse cevap = request.response;
      Uri uri =request.uri;

      if(uri.toString()=="/ws"){

        WebSocketTransformer.upgrade(request).then((WebSocket socket){
          socket.listen((data){

            print("Gelen Data $data");

          });
        });

      }else{
      cevap.write("Web socket server a girilmez");
      cevap.close();
      }

    });
  });
}
