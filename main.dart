import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

const apiBase = String.fromEnvironment('API_BASE', defaultValue: 'http://10.0.2.2:8000');

void main() {
  runApp(const RwhApp());
}

class RwhApp extends StatelessWidget {
  const RwhApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RWH MVP',
      theme: ThemeData(useMaterial3: true),
      home: const LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});
  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailCtrl = TextEditingController();
  final passCtrl = TextEditingController();
  final storage = const FlutterSecureStorage();
  String? error;

  Future<void> login() async {
    setState(() { error = null; });
    final res = await http.post(Uri.parse('$apiBase/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': emailCtrl.text, 'password': passCtrl.text})
    );
    if (res.statusCode == 200) {
      final tok = jsonDecode(res.body)['access_token'];
      await storage.write(key: 'token', value: tok);
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const SiteFormPage()));
    } else {
      setState(() { error = 'Login failed'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: emailCtrl, decoration: const InputDecoration(labelText: 'Email')),
            TextField(controller: passCtrl, decoration: const InputDecoration(labelText: 'Password'), obscureText: true),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: login, child: const Text('Login')),
            if (error != null) Text(error!, style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 12),
            TextButton(onPressed: () async {
              final res = await http.post(Uri.parse('$apiBase/auth/register'),
                headers: {'Content-Type': 'application/json'},
                body: jsonEncode({'name': 'Field User', 'email': emailCtrl.text, 'password': passCtrl.text})
              );
              if (res.statusCode == 200) {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Registered. Now log in.')));
              } else {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Registration failed')));
              }
            }, child: const Text('Register new user'))
          ],
        ),
      ),
    );
  }
}

class SiteFormPage extends StatefulWidget {
  const SiteFormPage({super.key});
  @override
  State<SiteFormPage> createState() => _SiteFormPageState();
}

class _SiteFormPageState extends State<SiteFormPage> {
  final latCtrl = TextEditingController();
  final lonCtrl = TextEditingController();
  final areaCtrl = TextEditingController();
  final rainfallCtrl = TextEditingController(text: '800'); // example
  String roofMaterial = 'concrete';
  String soilType = 'loam';
  Map<String, dynamic>? result;
  String? error;

  Future<String?> _token() async {
    const storage = FlutterSecureStorage();
    return await storage.read(key: 'token');
  }

  Future<void> submit() async {
    setState(() { error = null; result = null; });
    final token = await _token();
    if (token == null) { setState(() { error = 'Not logged in'; }); return; }

    final headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'};
    final siteRes = await http.post(Uri.parse('$apiBase/sites/'),
      headers: headers,
      body: jsonEncode({
        'latitude': double.tryParse(latCtrl.text) ?? 0,
        'longitude': double.tryParse(lonCtrl.text) ?? 0,
        'roof_area_sqm': double.tryParse(areaCtrl.text) ?? 0,
        'roof_material': roofMaterial,
        'soil_type': soilType,
        'avg_rainfall_mm': double.tryParse(rainfallCtrl.text) ?? 0
      }));
    if (siteRes.statusCode != 200) {
      setState(() { error = 'Failed to create site'; });
      return;
    }
    final siteId = jsonDecode(siteRes.body)['id'];
    final compRes = await http.post(Uri.parse('$apiBase/assessments/$siteId/compute'), headers: headers);
    if (compRes.statusCode == 200) {
      setState(() { result = jsonDecode(compRes.body); });
    } else {
      setState(() { error = 'Compute failed'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Site Assessment')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: latCtrl, decoration: const InputDecoration(labelText: 'Latitude')),
            TextField(controller: lonCtrl, decoration: const InputDecoration(labelText: 'Longitude')),
            TextField(controller: areaCtrl, decoration: const InputDecoration(labelText: 'Roof Area (sqm)')),
            TextField(controller: rainfallCtrl, decoration: const InputDecoration(labelText: 'Avg Rainfall (mm/yr)')),
            const SizedBox(height: 10),
            DropdownButton<String>(
              value: roofMaterial,
              items: const [
                DropdownMenuItem(value: 'concrete', child: Text('Concrete')),
                DropdownMenuItem(value: 'tile', child: Text('Tile')),
                DropdownMenuItem(value: 'metal', child: Text('Metal')),
                DropdownMenuItem(value: 'green_roof', child: Text('Green Roof')),
              ],
              onChanged: (v) => setState(() { roofMaterial = v!; }),
            ),
            DropdownButton<String>(
              value: soilType,
              items: const [
                DropdownMenuItem(value: 'loam', child: Text('Loam')),
                DropdownMenuItem(value: 'sand', child: Text('Sand')),
                DropdownMenuItem(value: 'clay', child: Text('Clay')),
              ],
              onChanged: (v) => setState(() { soilType = v!; }),
            ),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: submit, child: const Text('Compute')),
            if (error != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(error!, style: const TextStyle(color: Colors.red))),
            if (result != null) Padding(
              padding: const EdgeInsets.only(top: 16),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Harvest Potential (L/yr): ${result!['harvest_potential_lpy'].toStringAsFixed(2)}'),
                      Text('Recharge Feasible: ${result!['recharge_feasible']}'),
                      Text('Cost Estimate (INR): ${result!['cost_estimate_inr']}'),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
