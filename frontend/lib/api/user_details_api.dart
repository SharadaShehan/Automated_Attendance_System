import '../models/user.dart';
import 'package:http/http.dart' as http;

class UserDetailsApi {
  static Future<User?> getUserDetails(String token) async {
    final response = await http.get(
      Uri.parse('http://35.207.196.99/api/employee/view/employee/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Token $token'
      },
    );
    if (response.statusCode == 200) {
      return userFromJson(response.body);
    }
    if (response.statusCode == 401) {
      return null;
    } else {
      throw Exception('Failed to load user details');
    }
  }
}
