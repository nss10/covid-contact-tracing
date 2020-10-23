import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:barcode_scan/barcode_scan.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';
import 'package:intl/intl_standalone.dart';
// import 'package:flutter_nfc_reader/flutter_nfc_reader.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'Covid Contact Tracing'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var _result = "Please Scan the QR code";

  static final dateFormat = new DateFormat('MMM d, yyyy hh:mm aaa');
  Map<String, dynamic> _response;
  Map<String, dynamic> responseTitles = {
    "name": "Room Name",
    "current_strength": "Current Strength",
    "max_capacity": "Max Capacity",
    "last_sanitized_time": "Last Sanitized Time",
  };
  // NfcData _nfcData;
  Future<http.Response> _sendRequest() async {
    print(new DateTime.now().millisecondsSinceEpoch.toString());

    var _result_split = new List(2);
    _result_split = _result.split("-");

    http.Response response = await http.post(
      'http://<your-ip-address>:5000/addEvent',
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'room_id': _result_split[0],
        'user_id': '70983',
        'status': _result_split[1],
        'timestamp': new DateTime.now().millisecondsSinceEpoch.toString()
      }),
    );
    setState(() {
      _response = jsonDecode(utf8.decode(response.bodyBytes));
      if (_response['last_sanitized_time'] != null) {
        _response['last_sanitized_time'] =
            dateFormat.format(DateTime.parse(_response['last_sanitized_time']));
      }
    });
    print("State updated!");
    print(_response);
  }

  Future _scanQR() async {
    try {
      var qrResult = await BarcodeScanner.scan();
      setState(() {
        _result = qrResult.rawContent;
        _sendRequest();
      });
    } on PlatformException catch (e) {
      if (e.code == BarcodeScanner.cameraAccessDenied) {
        setState(() {
          _result = "Camera permission denied!";
        });
      }
    }
  }

  Padding getTableElement(String value) {
    return Padding(
      padding: const EdgeInsets.all(15),
      child: Text(
        value,
        style: TextStyle(color: Colors.blue, fontSize: 20),
        textAlign: TextAlign.left,
      ),
    );
  }

  List<Widget> populateCard() {
    List<Widget> entryCard = new List<Widget>();
    if (_response == null) {
      entryCard.add(Image.network(
        'https://www.clipartkey.com/mpngs/m/229-2295584_qr-code-scan-hand-scan-qr-code-png.png',
        fit: BoxFit.fill,
      ));
    } else if (_response['code'] == 200) {
      entryCard.add(getTableElement("Thank you for scanning!"));
    } else {
      responseTitles.forEach(
          (k, v) => entryCard.add(getTableElement("$v : ${_response[k]}")));
    }
    return entryCard;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Card(
              elevation: 10,
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: populateCard()),
            ),
            SizedBox(height: 50),
            RaisedButton.icon(
                color: Colors.blue,
                textColor: Colors.white,
                disabledColor: Colors.grey,
                disabledTextColor: Colors.black,
                padding: EdgeInsets.all(12.0),
                splashColor: Colors.blueAccent,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(25.0),
                ),
                onPressed: _scanQR,
                label: Text(
                  "Scan QR",
                  style: TextStyle(fontFamily: 'Times New Roman', fontSize: 23),
                ),
                icon: Icon(Icons.camera_alt))
          ],
        ),
      ),
    );
  }
}
