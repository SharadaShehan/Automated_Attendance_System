import '../models/user_attendance.dart';
import 'package:http/http.dart' as http;

class AttendanceByDateApi {
  static Future<List<UserAttendance>?> getAttendanceByDate(
      String token, String date) async {
    String year = date.substring(0, 4);
    String month = date.substring(5, 7);
    String day = date.substring(8, 10);
    final response = await http.get(
      Uri.parse(
          "http://35.207.196.99/api/executive/view/attendance/$year/$month/$day"),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Token $token'
      },
    );

    if (response.statusCode == 200) {
      return userAttendanceFromJson(response.body);
    } else if (response.statusCode == 401) {
      return null;
    } else {
      throw Exception('Failed to load attendance by date');
    }
  }
}
