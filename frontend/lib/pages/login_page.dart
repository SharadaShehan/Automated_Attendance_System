import 'package:flutter/material.dart';
import 'package:frontend/utilities/persistent_store.dart';
import '../models/login.dart';
import '../models/user.dart';
import '../api/login_api.dart';
import '../api/user_details_api.dart';
import 'package:provider/provider.dart';
import '../utilities/providers.dart';
import 'package:animate_do/animate_do.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  String invalidCredentialsMsg = "Invalid Credentials";
  bool displayMsg = false;
  bool isLoading = false;

  signIn(GlobalVariablesProvider provider) async {
    setState(() {
      displayMsg = false;
      isLoading = true;
    });
    AccessToken? token =
        await LoginApi.login(_emailController.text, _passwordController.text);
    if (token == null) {
      setState(() {
        displayMsg = true;
        isLoading = false;
      });
      return;
    }
    await setToken(token.token);
    User? user = await UserDetailsApi.getUserDetails(token.token);
    if (user == null) {
      setState(() {
        displayMsg = true;
        isLoading = false;
      });
      return;
    }
    provider.setAdmin(user.hasReadPermission);
    provider.setUser(user);
    provider.updateLogin();
    await setUserId(user.id);
    if (this.mounted) {
      setState(() {
        isLoading = false;
      });
    }
    int? userId = await getUserId();
    print("user id : $userId");
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    return isLoading
        ? const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          )
        : Scaffold(
            body: Container(
              width: double.infinity,
              decoration: BoxDecoration(
                  gradient: LinearGradient(begin: Alignment.topCenter, colors: [
                Colors.blue.shade600,
                Colors.blue.shade400,
                Colors.blue.shade200
              ])),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  const SizedBox(
                    height: 100,
                  ),
                  Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        FadeInUp(
                            duration: const Duration(milliseconds: 1000),
                            child: const Text(
                              "Login",
                              style:
                                  TextStyle(color: Colors.white, fontSize: 40),
                            )),
                        const SizedBox(
                          height: 10,
                        ),
                        FadeInUp(
                            duration: const Duration(milliseconds: 1300),
                            child: const Text(
                              "Welcome Back",
                              style:
                                  TextStyle(color: Colors.white, fontSize: 18),
                            )),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),
                  Expanded(
                    child: Container(
                      decoration: const BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.only(
                              topLeft: Radius.circular(60),
                              topRight: Radius.circular(60))),
                      child: Padding(
                        padding: const EdgeInsets.all(30),
                        child: Column(
                          children: <Widget>[
                            const SizedBox(
                              height: 60,
                            ),
                            FadeInUp(
                                duration: const Duration(milliseconds: 1400),
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.white,
                                      borderRadius: BorderRadius.circular(10),
                                      boxShadow: const [
                                        BoxShadow(
                                            color:
                                                Color.fromRGBO(27, 95, 225, .4),
                                            blurRadius: 20,
                                            offset: Offset(0, 10))
                                      ]),
                                  child: Column(
                                    children: <Widget>[
                                      Container(
                                        padding: const EdgeInsets.all(10),
                                        decoration: BoxDecoration(
                                            border: Border(
                                                bottom: BorderSide(
                                                    color:
                                                        Colors.grey.shade200))),
                                        child: TextField(
                                          decoration: const InputDecoration(
                                              hintText: "Email",
                                              hintStyle:
                                                  TextStyle(color: Colors.grey),
                                              border: InputBorder.none),
                                          controller: _emailController,
                                        ),
                                      ),
                                      Container(
                                        padding: const EdgeInsets.all(10),
                                        decoration: BoxDecoration(
                                            border: Border(
                                                bottom: BorderSide(
                                                    color:
                                                        Colors.grey.shade200))),
                                        child: TextField(
                                          obscureText: true,
                                          decoration: const InputDecoration(
                                              hintText: "Password",
                                              hintStyle:
                                                  TextStyle(color: Colors.grey),
                                              border: InputBorder.none),
                                          controller: _passwordController,
                                        ),
                                      ),
                                    ],
                                  ),
                                )),
                            if (displayMsg)
                              const SizedBox(
                                height: 20,
                              ),
                            if (displayMsg)
                              FadeInUp(
                                  duration: const Duration(milliseconds: 200),
                                  child: const Text(
                                    "Invalid Credentials",
                                    style: TextStyle(
                                        color: Color.fromRGBO(244, 67, 54, 1)),
                                  )),
                            if (!displayMsg)
                              const SizedBox(
                                height: 40,
                              ),
                            if (displayMsg)
                              const SizedBox(
                                height: 20,
                              ),
                            FadeInUp(
                                duration: const Duration(milliseconds: 1500),
                                child: const Text(
                                  "Forgot Password?",
                                  style: TextStyle(color: Colors.grey),
                                )),
                            const SizedBox(
                              height: 40,
                            ),
                            FadeInUp(
                                duration: const Duration(milliseconds: 500),
                                child: MaterialButton(
                                  onPressed: () {
                                    signIn(provider);
                                  },
                                  height: 50,
                                  // margin: EdgeInsets.symmetric(horizontal: 50),
                                  color: Colors.blue.shade500,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(50),
                                  ),
                                  // decoration: BoxDecoration(
                                  // ),
                                  child: const Center(
                                    child: Text(
                                      "Login",
                                      style: TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                )),
                            const SizedBox(
                              height: 50,
                            ),
                          ],
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          );
  }
}
