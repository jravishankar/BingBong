import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:video_player/video_player.dart';
import 'package:image_picker/image_picker.dart';
import 'package:spring_button/spring_button.dart';
import 'package:path/path.dart';
import 'package:video_record_upload/api/firebase_api.dart';
import 'package:video_record_upload/review.dart';

class ProVideo extends StatefulWidget{
  const ProVideo({Key? key}) : super(key: key);

  @override
  State<ProVideo> createState() => _ProVideoState();
}

class _ProVideoState extends State<ProVideo> {
  final ImagePicker _picker = ImagePicker();
  VideoPlayerController? _controller;

  @override
  void initState() {
    _controller = VideoPlayerController.asset('assets/forehand_shakehold.mp4');
    _controller?.initialize().then((_) {
      // 最初のフレームを描画するため初期化後に更新
      setState(() {});
      _controller?.setLooping(true);
      _controller?.setVolume(0);
      _controller?.play();
    });
    super.initState();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  void deactivate() {
    _controller?.pause();
    super.deactivate();
  }

  Widget menuButton(BuildContext context) {
    return SizedBox(
      height: 85,
      width: 125,
      child: SpringButton(
        SpringButtonType.WithOpacity,
        Padding(
          padding: const EdgeInsets.all(14),
          child: Container(
            decoration: const BoxDecoration(
              color: Color.fromRGBO(0, 26, 67, 1),
              borderRadius: BorderRadius.all(Radius.circular(30.0)),
            ),
            child: Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(
                    Icons.arrow_back,
                    color: Colors.white,
                    size: 30,
                  ),
                  Text(
                    '戻る',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 20,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        onTap: () async {
          await Future.delayed(const Duration(milliseconds: 80));
          Navigator.pop(context);
        }
      ),
    );
  }

  Widget cameraButton(BuildContext context) {
    return SizedBox(
      height: 100,
      width: 250,
      child: SpringButton(
        SpringButtonType.WithOpacity,
        Padding(
          padding: const EdgeInsets.all(12.5),
          child: Container(
            decoration: const BoxDecoration(
              color: Color.fromRGBO(125, 2, 10, 1.0),
              borderRadius: BorderRadius.all(Radius.circular(10.0)),
            ),
            child: Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(
                    Icons.videocam_rounded,
                    color: Colors.white,
                    size: 45,
                  ),
                  Text(
                    '動画を撮影',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 25,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        onTap: () async {
          await Future.delayed(const Duration(milliseconds: 60));
          await _controller?.pause();
          final XFile? file = await _picker.pickVideo(
              source: ImageSource.camera,
              maxDuration: const Duration(seconds: 10)
          );
          print("kokoniiruyo!!!!!!!");
          setState(() {

          });

          //動画を撮影しなかったときの処理
          if(file != null) {
            await Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => Review(file)),
            ).then((value) async {
              print("1");
              //_controller = VideoPlayerController.asset('assets/water.mp4');
              print("2");
            });
          }

          //await _controller?.initialize();
          await _controller?.setLooping(true);
          await _controller?.play();
          print("4");
          //戻ってくるときにcontrollerをdisposeする必要がありそう

          print("Video Path ${file!.path}");
          //_controller?.play();
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          //ここでプロの動画を再生したい
          VideoPlayer(_controller!),
          Align(
            alignment: const Alignment(0, 1.02),
            child: cameraButton(context),
          ),
          Align(
            alignment: const Alignment(-0.87, 1.02),
            child: menuButton(context),
          ),
        ],
      ),
    );
  }
}