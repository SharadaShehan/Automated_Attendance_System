import 'package:flutter/material.dart';
import 'utilities/providers.dart';
import 'pages/login_page.dart';
import 'package:provider/provider.dart';
import 'pages/home_page.dart';

void main() async {
  runApp(
    ChangeNotifierProvider(
      create: (_) => GlobalVariablesProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);

    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: Scaffold(
        body: provider.isLoggedIn ? const HomePage() : const LoginPage(),
      ),
    );
  }
}
