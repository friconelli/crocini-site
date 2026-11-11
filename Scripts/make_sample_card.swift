// Biglietto da visita di esempio (91×61 mm = 85×55 + 3 mm di abbondanza, 300 dpi) per gli screenshot del sito.
import AppKit
let out = CommandLine.arguments[1]
let fontURL = URL(fileURLWithPath: CommandLine.arguments[2]) as CFURL
CTFontManagerRegisterFontsForURL(fontURL, .process, nil)

let mm = 72.0 / 25.4          // punti per millimetro: si disegna in punti, 1 punto = 300/72 pixel
let w = 91 * mm, h = 61 * mm
let scale = 300.0 / 72.0
let pw = Int((w * scale).rounded()), ph = Int((h * scale).rounded())
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
let cg = CGContext(data: nil, width: pw, height: ph, bitsPerComponent: 8, bytesPerRow: 0, space: cs,
                   bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
cg.scaleBy(x: scale, y: scale)
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)

NSColor(red: 1.0, green: 0.95, blue: 0.90, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: w, height: h).fill()
// cerchio magenta che esce dal bordo (serve l'abbondanza)
NSColor(red: 0.93, green: 0.13, blue: 0.47, alpha: 1).setFill()
NSBezierPath(ovalIn: NSRect(x: w * 0.66, y: -h * 0.25, width: h * 1.25, height: h * 1.25)).fill()
NSColor(red: 0.10, green: 0.07, blue: 0.10, alpha: 1).setFill()
NSBezierPath(ovalIn: NSRect(x: w * 0.84, y: h * 0.62, width: h * 0.42, height: h * 0.42)).fill()

func text(_ s: String, size: CGFloat, weight: NSFont.Weight, color: NSColor, at p: NSPoint) {
    let f = NSFont(name: "Bricolage Grotesque", size: size).map { NSFontManager.shared.convert($0, toHaveTrait: weight.rawValue > 0.3 ? .boldFontMask : []) }
        ?? NSFont.systemFont(ofSize: size, weight: weight)
    s.draw(at: p, withAttributes: [.font: f, .foregroundColor: color])
}
let ink = NSColor(red: 0.10, green: 0.07, blue: 0.10, alpha: 1)
text("Bottega Fontana", size: 14.5, weight: .heavy, color: ink, at: NSPoint(x: 15 * mm / 1.0, y: h - 27 * mm))
text("Ceramiche artigianali", size: 8.5, weight: .regular, color: ink.withAlphaComponent(0.75), at: NSPoint(x: 15 * mm, y: h - 35 * mm))
text("Lucia Fontana", size: 8, weight: .semibold, color: ink, at: NSPoint(x: 15 * mm, y: 17 * mm))
text("lucia@bottegafontana.example", size: 7, weight: .regular, color: ink.withAlphaComponent(0.7), at: NSPoint(x: 15 * mm, y: 11.5 * mm))
NSGraphicsContext.restoreGraphicsState()

// PNG con i 300 dpi dichiarati nel file (così Crocini ne ricava la misura reale in mm).
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, [kCGImagePropertyDPIWidth: 300, kCGImagePropertyDPIHeight: 300] as CFDictionary)
CGImageDestinationFinalize(dest)
