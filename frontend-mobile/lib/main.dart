import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Image Detector',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: Color(0xFF0D0D0D),
        primaryColor: Colors.blueAccent,
        colorScheme: ColorScheme.dark(
          primary: Colors.blueAccent,
          secondary: Colors.purpleAccent,
          surface: Color(0xFF1A1A1A),
        ),
        useMaterial3: true,
      ),
      home: DetectorScreen(),
    );
  }
}

class DetectorScreen extends StatefulWidget {
  @override
  _DetectorScreenState createState() => _DetectorScreenState();
}

class _DetectorScreenState extends State<DetectorScreen> {
  final ImagePicker _picker = ImagePicker();
  File? _image;
  Map<String, dynamic>? _result;
  bool _isLoading = false;
  String? _error;

  // Use 10.0.2.2 for Android Emulator, localhost for iOS simulator, or IP for physical device
  // Change this to your PC's local IP (e.g., 192.168.1.x) for physical devices
  final String _apiUrl = Platform.isAndroid 
      ? "http://10.0.2.2:8000/detect" 
      : "http://127.0.0.1:8000/detect";

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? pickedFile = await _picker.pickImage(source: source);
      if (pickedFile != null) {
        setState(() {
          _image = File(pickedFile.path);
          _result = null;
          _error = null;
        });
        await _analyzeImage();
      }
    } catch (e) {
      setState(() {
        _error = "Failed to pick image: $e";
      });
    }
  }

  Future<void> _analyzeImage() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      var request = http.MultipartRequest("POST", Uri.parse(_apiUrl));
      request.files.add(await http.MultipartFile.fromPath("file", _image!.path));

      var response = await request.send();

      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        setState(() {
          _result = json.decode(responseData);
        });
      } else {
        setState(() {
          _error = "Server Error: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _error = "Connection Failed. Is backend running? ($e)";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("AI Authenticator", style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Image Preview Area
              Container(
                height: 300,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white10),
                ),
                child: _image != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(16),
                        child: Image.file(_image!, fit: BoxFit.cover),
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.add_photo_alternate_rounded, size: 60, color: Colors.grey),
                          SizedBox(height: 10),
                          Text("No Image Selected", style: TextStyle(color: Colors.grey)),
                        ],
                      ),
              ),
              
              SizedBox(height: 20),

              // Action Buttons
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      icon: Icon(Icons.camera_alt),
                      label: Text("Camera"),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(vertical: 15),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: _isLoading ? null : () => _pickImage(ImageSource.camera),
                    ),
                  ),
                  SizedBox(width: 15),
                  Expanded(
                    child: ElevatedButton.icon(
                      icon: Icon(Icons.photo_library),
                      label: Text("Gallery"),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(vertical: 15),
                        backgroundColor: Colors.grey[800],
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: _isLoading ? null : () => _pickImage(ImageSource.gallery),
                    ),
                  ),
                ],
              ),

              SizedBox(height: 30),

              // Loading State
              if (_isLoading)
                Column(
                  children: [
                    CircularProgressIndicator(),
                    SizedBox(height: 10),
                    Text("Analyzing pixel patterns...", style: TextStyle(color: Colors.white70)),
                  ],
                ),

              // Error Message
              if (_error != null)
                Container(
                  padding: EdgeInsets.all(15),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.redAccent.withOpacity(0.3)),
                  ),
                  child: Text(_error!, style: TextStyle(color: Colors.redAccent)),
                ),

              // Results Area
              if (_result != null && !_isLoading) ...[
                Text("Analysis Result", style: TextStyle(fontSize: 18, color: Colors.white54)),
                SizedBox(height: 10),
                
                // Verdict Card
                Container(
                  padding: EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.surface,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(
                      color: _result!["result"] == "Real" ? Colors.green : Colors.red,
                      width: 1,
                    ),
                  ),
                  child: Column(
                    children: [
                      Text(
                        _result!["result"].toString().toUpperCase(),
                        style: TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.w900,
                          color: _result!["result"] == "Real" ? Colors.greenAccent : Colors.redAccent,
                          letterSpacing: 1.5,
                        ),
                      ),
                      SizedBox(height: 5),
                      Text(
                        "${_result!['confidence']}% Confidence",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ),

                SizedBox(height: 20),

                // Heatmap Display
                if (_result!["heatmap"] != null) ...[
                  Text("Visual Heatmap", style: TextStyle(fontSize: 18, color: Colors.white54)),
                  SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(12),
                    child: Image.memory(
                      base64Decode(_result!["heatmap"]),
                      fit: BoxFit.cover,
                    ),
                  ),
                ],
              ],
            ],
          ),
        ),
      ),
    );
  }
}
