import 'dart:io';

import 'package:flutter/material.dart';
import 'package:video_record_upload/pro_video.dart';

const MaterialColor customSwatch = MaterialColor(
  0xFFB71C1C,
  <int, Color>{
    50: Color(0xFFFFEBEE),
    100: Color(0xFFFFCDD2),
    200: Color(0xFFEF9A9A),
    300: Color(0xFFE57373),
    400: Color(0xFFEF5350),
    500: Color(0xFFF44336),
    600: Color(0xFFE53935),
    700: Color(0xFFD32F2F),
    800: Color(0xFFC62828),
    900: Color(0xFFB71C1C),
  },
);

class Menu extends StatelessWidget {
  const Menu({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // 右上に表示される"debug"ラベルを消す
      debugShowCheckedModeBanner: false,
      // アプリ名
      title: 'BingBong',
      theme: ThemeData(
        // テーマカラー
        primarySwatch: customSwatch,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      // リスト一覧画面を表示
      home: const Menupage(),
    );
  }
}

// リスト一覧画面用Widget
class Menupage extends StatefulWidget {
  const Menupage({Key? key}) : super(key: key);

  @override
  _MenuPageState createState() => _MenuPageState();
}

class _MenuPageState extends State<Menupage> {
  // ignore: non_constant_identifier_names
  Widget VideoInfo() {
    return Column(
      children: [
        const Padding(
          padding: EdgeInsets.fromLTRB(1, 5, 1, 5),
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            const Image(
              image: AssetImage("assets/image/image004.jpg"),
              width: 250,
              height: 125,
              fit: BoxFit.fill,
            ),
            const Image(
              image: AssetImage("assets/image/image001.jpg"),
              width: 250,
              height: 125,
              fit: BoxFit.fill,
            ),
            ElevatedButton(
              child: const Text('選択'),
              style: ElevatedButton.styleFrom(
                primary: Colors.white,
                onPrimary: Colors.black,
                shape: const CircleBorder(
                  side: BorderSide(
                    color: Colors.black,
                    width: 1,
                    style: BorderStyle.solid,
                  ),
                ),
              ),
              onPressed: () async {
                await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ProVideo()),
                );
              },
            ),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromRGBO(255, 215, 130, 1),
      // AppBarを表示し、タイトルも設定
      appBar: AppBar(
        automaticallyImplyLeading: false,
        centerTitle: true,
        title: const Image(
          image: AssetImage("assets/image/image003.jpg"),
          width: 50,
          height: 25,
          fit: BoxFit.fill,
        ),
        actions: <Widget>[
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.search),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.more_vert),
          ),
        ],
      ),
      // データを元にListViewを作成
      body: Center(
        child: Container(
          color: const Color.fromRGBO(255, 215, 130, 1),
          height: 500,
          width: double.infinity,
          child: SingleChildScrollView(
            child: Column(
              children: <Widget>[
                for (int i = 0; i < 3; i++) VideoInfo(),
                const Padding(
                  padding: EdgeInsets.fromLTRB(1, 5, 1, 5),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
