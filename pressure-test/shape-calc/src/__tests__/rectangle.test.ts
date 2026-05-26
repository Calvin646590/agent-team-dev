import { describe, it, expect } from "vitest";
import { Point } from "../geometry/point.js";
import { Rectangle } from "../geometry/rectangle.js";
import { area } from "../geometry/area.js";
import { perimeter } from "../geometry/perimeter.js";

describe("Rectangle", () => {
  const topLeft = new Point(0, 0);
  const rect = new Rectangle(topLeft, 10, 5);

  it("area: width * height", () => {
    expect(rect.area()).toBe(50);
  });

  it("perimeter: 2 * (width + height)", () => {
    expect(rect.perimeter()).toBe(30);
  });

  it("contains: 内部点", () => {
    const inside = new Point(5, 2);
    expect(rect.contains(inside)).toBe(true);
  });

  it("contains: topLeft 角点（边界包含）", () => {
    const corner = new Point(0, 0);
    expect(rect.contains(corner)).toBe(true);
  });

  it("contains: 右下角点（边界包含）", () => {
    const bottomRight = new Point(10, 5);
    expect(rect.contains(bottomRight)).toBe(true);
  });

  it("contains: 外部点（x 越界）", () => {
    const outsideX = new Point(11, 2);
    expect(rect.contains(outsideX)).toBe(false);
  });

  it("contains: 外部点（y 越界）", () => {
    const outsideY = new Point(5, 6);
    expect(rect.contains(outsideY)).toBe(false);
  });

  it("非正宽度抛 Error", () => {
    expect(() => new Rectangle(new Point(0, 0), 0, 5)).toThrow("width must be positive");
    expect(() => new Rectangle(new Point(0, 0), -3, 5)).toThrow("width must be positive");
  });

  it("非正高度抛 Error", () => {
    expect(() => new Rectangle(new Point(0, 0), 10, 0)).toThrow("height must be positive");
    expect(() => new Rectangle(new Point(0, 0), 10, -2)).toThrow("height must be positive");
  });

  it("toString: 格式正确", () => {
    expect(rect.toString()).toBe("Rectangle(Point(0, 0), 10×5)");
  });

  it("不同 topLeft 的 toString 格式", () => {
    const r2 = new Rectangle(new Point(3, 4), 6, 2);
    expect(r2.toString()).toBe("Rectangle(Point(3, 4), 6×2)");
  });
});

describe("area/perimeter - Rectangle", () => {
  const topLeft = new Point(1, 1);
  const rect = new Rectangle(topLeft, 8, 3);

  it("area(rect) 等于 rect.area()", () => {
    expect(area(rect)).toBe(rect.area());
    expect(area(rect)).toBe(24);
  });

  it("perimeter(rect) 等于 rect.perimeter()", () => {
    expect(perimeter(rect)).toBe(rect.perimeter());
    expect(perimeter(rect)).toBe(22);
  });
});
