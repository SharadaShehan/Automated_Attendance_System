import '../models/login.dart';
import 'package:http/http.dart' as http;

class LoginApi {
  static Future<AccessToken?> login(String email, String password) async {
    final data = LoginData(email: email, password: password);
    final response = await http.post(
      Uri.parse('http://35.207.196.99/api/auth/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: loginDataToJson(data),
    );

    if (response.statusCode == 200) {
      return accessTokenFromJson(response.body);
    } else if (response.statusCode == 400) {
      return null;
    } else {
      throw Exception('Failed to login');
    }
  }
}
