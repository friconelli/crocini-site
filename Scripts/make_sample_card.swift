// Biglietto da visita di esempio GENERICO (91×61 mm = 85×55 + 3 mm di abbondanza, 300 dpi): nessun nome né testo,
// solo forme e segnaposto grigi al posto delle righe di testo. Serve per le immagini del sito.  uso: out.png
import AppKit
let out = CommandLine.arguments[1]
let mm = 72.0 / 25.4
let w = 91 * mm, h = 61 * mm
let scale = 300.0 / 72.0
let pw = Int((w * scale).rounded()), ph = Int((h * scale).rounded())
let cg = CGContext(data: nil, width: pw, height: ph, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                   bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
cg.scaleBy(x: scale, y: scale)
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)

let ink = NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1)
NSColor(red: 1.0, green: 0.95, blue: 0.90, alpha: 1).setFill(); NSRect(x: 0, y: 0, width: w, height: h).fill()
// cerchi che escono dal bordo (servono l'abbondanza)
NSColor(red: 0.925, green: 0, blue: 0.549, alpha: 1).setFill()
NSBezierPath(ovalIn: NSRect(x: w * 0.62, y: -h * 0.28, width: h * 1.3, height: h * 1.3)).fill()
ink.setFill()
NSBezierPath(ovalIn: NSRect(x: w * 0.82, y: h * 0.64, width: h * 0.42, height: h * 0.42)).fill()

func bar(_ x: Double, _ y: Double, _ bw: Double, _ bh: Double, _ alpha: CGFloat) {
    ink.withAlphaComponent(alpha).setFill()
    NSBezierPath(roundedRect: NSRect(x: x * mm, y: y * mm, width: bw * mm, height: bh * mm), xRadius: bh * mm / 2, yRadius: bh * mm / 2).fill()
}
// segnaposto del testo: un piccolo simbolo, un titolo, un sottotitolo e tre righe di contatti
ink.setFill()
NSBezierPath(ovalIn: NSRect(x: 12 * mm, y: 40 * mm, width: 6 * mm, height: 6 * mm)).fill()
bar(12, 30, 32, 4.2, 1)       // titolo
bar(12, 24, 22, 2.4, 0.35)    // sottotitolo
bar(12, 15, 26, 1.6, 0.5)     // contatti
bar(12, 11.5, 20, 1.6, 0.5)
bar(12, 8, 24, 1.6, 0.5)
NSGraphicsContext.restoreGraphicsState()
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, [kCGImagePropertyDPIWidth: 300, kCGImagePropertyDPIHeight: 300] as CFDictionary)
CGImageDestinationFinalize(dest)
