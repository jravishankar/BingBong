import 'package:http/http.dart' as http;

class PythonApi {
  static Future<http.Response> fetchImprovement(String url) {
    return http.get(Uri.parse(url));
  }
}