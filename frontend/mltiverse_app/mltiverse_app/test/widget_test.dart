// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:mltiverse_app/main.dart';

void main() {
  testWidgets('Welcome screen UI components test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const EpicVerseApp());

    // Verify that branding and titles are present
    expect(find.text('VOICE COMPANION'), findsOneWidget);
    expect(find.text('To begin your journey, create your Companion identity.'), findsOneWidget);

    // Verify buttons are present
    expect(find.text('Create Companion Profile'), findsOneWidget);
    expect(find.text('Resume Journey (Sign In)'), findsOneWidget);
  });
}
