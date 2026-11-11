// Grafica quadrata di esempio GENERICA (tre "lastre" C M Y sfalsate e un punto nero, nessun testo) che regge
// ritagli molto stretti: per gli elementi con proporzioni lontane dal biglietto (segnalibri, flyer DL…).  uso: out.png
import AppKit
let out = CommandLine.arguments[1]
let N = 1000
let cg = CGContext(data: nil, width: N, height: N, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                   bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)
NSColor(red: 1.0, green: 0.95, blue: 0.90, alpha: 1).setFill(); NSRect(x: 0, y: 0, width: N, height: N).fill()
func disc(_ color: NSColor, _ x: CGFloat, _ y: CGFloat, _ d: CGFloat) { color.setFill(); NSBezierPath(ovalIn: NSRect(x: x, y: y, width: d, height: d)).fill() }
disc(NSColor(red: 0, green: 0.68, blue: 0.94, alpha: 1), 90, 175, 760)        // ciano
disc(NSColor(red: 1, green: 0.95, blue: 0, alpha: 1), 150, 105, 760)          // giallo
disc(NSColor(red: 0.925, green: 0, blue: 0.549, alpha: 0.92), 120, 140, 760)  // magenta (sovrapposto)
disc(NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1), 455, 880, 90)     // punto nero
disc(NSColor.white, 440, 440, 120)                                             // punto bianco al centro
NSGraphicsContext.restoreGraphicsState()
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, nil); CGImageDestinationFinalize(dest)
