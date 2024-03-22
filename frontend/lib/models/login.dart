import 'dart:convert';

String loginDataToJson(LoginData data) => json.encode(data.toJson());

class LoginData {
  String email;
  String password;

  LoginData({
    required this.email,
    required this.password,
  });

  factory LoginData.fromJson(Map<String, dynamic> json) => LoginData(
        email: json["email"],
        password: json["password"],
      );

  Map<String, dynamic> toJson() => {
        "email": email,
        "password": password,
      };
}

AccessToken accessTokenFromJson(String str) =>
    AccessToken.fromJson(json.decode(str));

class AccessToken {
  String token;

  AccessToken({
    required this.token,
  });

  factory AccessToken.fromJson(Map<String, dynamic> json) => AccessToken(
        token: json["token"],
      );

  Map<String, dynamic> toJson() => {
        "token": token,
      };
}
