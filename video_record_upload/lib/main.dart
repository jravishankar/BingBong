import 'dart:io';

import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:video_player/video_player.dart';
import 'package:image_picker/image_picker.dart';
import 'package:spring_button/spring_button.dart';
import 'package:path/path.dart';
import 'package:video_record_upload/api/firebase_api.dart';
import 'package:video_record_upload/pro_video.dart';
import 'package:video_record_upload/menu.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft, //横固定
  ]);
  await Firebase.initializeApp();
  runApp(const Menu());
}
