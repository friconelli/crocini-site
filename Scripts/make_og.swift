// Immagine di anteprima social 1200×630: swift make_og.swift out.png icon.png font.ttf "Titolo" "Sottotitolo"
import AppKit
let a = CommandLine.arguments
CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: a[3]) as CFURL, .process, nil)
let W = 1200, H = 630
let cg = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                   space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(cgContext: cg, flipped: false)
NSColor.white.setFill(); NSRect(x: 0, y: 0, width: W, height: H).fill()
// barra quadricromia in basso
for (i, c) in [NSColor(red: 0, green: 0.68, blue: 0.94, alpha: 1), NSColor(red: 0.93, green: 0, blue: 0.55, alpha: 1),
               NSColor(red: 1, green: 0.95, blue: 0, alpha: 1), NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1)].enumerated() {
    c.setFill(); NSRect(x: CGFloat(i * W / 4), y: 0, width: CGFloat(W / 4), height: 30).fill()
}
// crocini neri di cornice
NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1).setStroke()
let m: CGFloat = 44, l: CGFloat = 70
let p = NSBezierPath(); p.lineWidth = 6; p.lineCapStyle = .square
for (x, y, dx, dy) in [(m, m + 30, 1.0, 1.0), (CGFloat(W) - m, m + 30, -1.0, 1.0), (m, CGFloat(H) - m, 1.0, -1.0), (CGFloat(W) - m, CGFloat(H) - m, -1.0, -1.0)] {
    p.move(to: NSPoint(x: x + dx * l, y: y)); p.line(to: NSPoint(x: x, y: y)); p.line(to: NSPoint(x: x, y: y + dy * l))
}
p.stroke()
if let icon = NSImage(contentsOfFile: a[2]) { icon.draw(in: NSRect(x: 110, y: 205, width: 250, height: 250)) }
func font(_ s: CGFloat, _ w: NSFont.Weight) -> NSFont {
    let f = NSFont(name: "Bricolage Grotesque", size: s) ?? NSFont.systemFont(ofSize: s, weight: w)
    return w.rawValue > 0.3 ? NSFontManager.shared.convert(f, toHaveTrait: .boldFontMask) : f
}
a[4].draw(at: NSPoint(x: 410, y: 300), withAttributes: [.font: font(136, .heavy), .foregroundColor: NSColor(red: 0.08, green: 0.08, blue: 0.08, alpha: 1)])
a[5].draw(at: NSPoint(x: 416, y: 238), withAttributes: [.font: font(44, .semibold), .foregroundColor: NSColor(red: 0.93, green: 0, blue: 0.55, alpha: 1)])
NSGraphicsContext.restoreGraphicsState()
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, "public.png" as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg.makeImage()!, nil); CGImageDestinationFinalize(dest)
