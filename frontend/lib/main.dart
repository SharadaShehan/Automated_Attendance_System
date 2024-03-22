import 'package:flutter/material.dart';
import 'utilities/providers.dart';
import 'pages/login_page.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => GlobalVariablesProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<GlobalVariablesProvider>(context);
    print('isLoggedIn: ${provider.isLoggedIn}');

    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: Scaffold(
        // appBar: AppBar(
        //   title: const Text('AttendSense'),

        // ),
        body: provider.isLoggedIn
            ? const Center(child: Text('Welcome!'))
            : LoginPage(),
      ),
    );
  }
}
