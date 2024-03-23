import '../models/user.dart';
import 'package:http/http.dart' as http;

class ViewEmployeeDetailsApi {
  static Future<User?> getEmployeeDetails(String token, int id) async {
    final response = await http.get(
      Uri.parse('http://35.207.196.99/api/executive/view/employee/$id'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Token $token'
      },
    );

    if (response.statusCode == 200) {
      return userFromJson(response.body);
    } else if (response.statusCode == 401) {
      return null;
    } else {
      throw Exception('Failed to load user details');
    }
  }
}
