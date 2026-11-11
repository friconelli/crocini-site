// Grafica quadrata di esempio (monogramma "BF" e cerchi) che regge ritagli molto stretti, per gli elementi
// con proporzioni lontane dal biglietto da visita: segnalibri, flyer DL, ecc.  uso: out.png font.ttf
import AppKit
let out = CommandLine.arguments[1]
CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: CommandLine.arguments[2]) as CFURL, .process, nil)
let N = 1000
let cg = CGContext(data: nil, width: N, height: N, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                   bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)
NSColor(red: 1.0, green: 0.95, blue: 0.90, alpha: 1).setFill(); NSRect(x: 0, y: 0, width: N, height: N).fill()
NSColor(red: 0.925, green: 0, blue: 0.549, alpha: 1).setFill()
NSBezierPath(ovalIn: NSRect(x: 100, y: 130, width: 800, height: 800)).fill()
NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1).setFill()
NSBezierPath(ovalIn: NSRect(x: 455, y: 880, width: 90, height: 90)).fill()
let f = NSFont(name: "Bricolage Grotesque", size: 250).map { NSFontManager.shared.convert($0, toHaveTrait: .boldFontMask) } ?? NSFont.boldSystemFont(ofSize: 250)
let t = "BF" as NSString
let attrs: [NSAttributedString.Key: Any] = [.font: f, .foregroundColor: NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1)]
let size = t.size(withAttributes: attrs)
t.draw(at: NSPoint(x: (CGFloat(N) - size.width) / 2, y: 470 - size.height / 2 + 40), withAttributes: attrs)
NSGraphicsContext.restoreGraphicsState()
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, nil); CGImageDestinationFinalize(dest)
