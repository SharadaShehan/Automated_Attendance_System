import 'dart:convert';

List<UserAttendance> userAttendanceFromJson(String str) =>
    List<UserAttendance>.from(
        json.decode(str).map((x) => UserAttendance.fromJson(x)));

class UserAttendance {
  List<String> entrance;
  List<String> leave;
  int id;
  String firstName;
  String lastName;

  UserAttendance({
    required this.entrance,
    required this.leave,
    required this.id,
    required this.firstName,
    required this.lastName,
  });

  factory UserAttendance.fromJson(Map<String, dynamic> json) => UserAttendance(
        entrance: List<String>.from(json["entrance"].map((x) => x)),
        leave: List<String>.from(json["leave"].map((x) => x)),
        id: json["id"],
        firstName: json["first_name"],
        lastName: json["last_name"],
      );

  Map<String, dynamic> toJson() => {
        "entrance": List<dynamic>.from(entrance.map((x) => x)),
        "leave": List<dynamic>.from(leave.map((x) => x)),
        "id": id,
        "first_name": firstName,
        "last_name": lastName,
      };
}
