import 'dart:convert';

User userFromJson(String str) => User.fromJson(json.decode(str));

String userToJson(User data) => json.encode(data.toJson());

class User {
  int id;
  String email;
  String roleName;
  bool hasReadPermission;
  bool hasEditPermission;
  String firstName;
  String lastName;
  dynamic picture;
  dynamic attendance;
  bool notifications;

  User({
    required this.id,
    required this.email,
    required this.roleName,
    required this.hasReadPermission,
    required this.hasEditPermission,
    required this.firstName,
    required this.lastName,
    this.picture,
    required this.attendance,
    required this.notifications,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json["id"],
        email: json["email"],
        roleName: json["role_name"],
        hasReadPermission: json["has_read_permission"],
        hasEditPermission: json["has_edit_permission"],
        firstName: json["first_name"],
        lastName: json["last_name"],
        picture: json["picture"],
        attendance: json["attendance"],
        notifications: json["notifications"],
      );

  Map<String, dynamic> toJson() => {
        "id": id,
        "email": email,
        "role_name": roleName,
        "has_read_permission": hasReadPermission,
        "has_edit_permission": hasEditPermission,
        "first_name": firstName,
        "last_name": lastName,
        "picture": picture,
        "attendance": attendance,
        "notifications": notifications,
      };
}
