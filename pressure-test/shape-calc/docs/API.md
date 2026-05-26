# shape-calc API Reference

> TypeScript 几何图形计算库

## 安装与使用

```bash
npm install
npm run build
```

```typescript
import { Point, Line, Circle, Rectangle } from "./src/geometry/point.js";
import { area, circleArea, rectangleArea } from "./src/geometry/area.js";
import { perimeter, lineLength, circleCircumference, rectanglePerimeter } from "./src/geometry/perimeter.js";
```

---

## Point

表示二维平面上的一个点。

### 构造函数

```typescript
constructor(x: number, y: number)
```

| 参数 | 类型     | 说明         |
|------|----------|--------------|
| `x`  | `number` | 点的横坐标   |
| `y`  | `number` | 点的纵坐标   |

创建后，`x` 和 `y` 均为只读属性（`readonly`）。

### 方法

#### `distanceTo(other: Point): number`

计算当前点到另一点之间的欧几里得距离。

**参数**

| 参数    | 类型    | 说明       |
|---------|---------|------------|
| `other` | `Point` | 目标点     |

**返回值**：`number` — 两点之间的距离（非负数）。

---

#### `toString(): string`

返回点的字符串表示，格式为 `Point(x, y)`。

**返回值**：`string` — 如 `"Point(3, 4)"`。

### 示例

```typescript
import { Point } from "./src/geometry/point.js";

const origin = new Point(0, 0);
const p = new Point(3, 4);

console.log(origin.distanceTo(p));  // 5
console.log(p.toString());          // "Point(3, 4)"

// 坐标为只读
console.log(p.x); // 3
console.log(p.y); // 4

// 负坐标
const q = new Point(-1, -1);
console.log(q.distanceTo(new Point(2, 3))); // 5
```

---

## Line

表示由两个端点定义的线段。

### 构造函数

```typescript
constructor(start: Point, end: Point)
```

| 参数    | 类型    | 说明       |
|---------|---------|------------|
| `start` | `Point` | 线段的起点 |
| `end`   | `Point` | 线段的终点 |

`start` 和 `end` 均为只读属性（`readonly`）。

### 方法

#### `length(): number`

计算线段的长度（即起点到终点的欧几里得距离）。

**返回值**：`number` — 线段长度（非负数）。

---

#### `slope(): number | null`

计算线段的斜率（rise / run）。若线段为垂直线（`start.x === end.x`），则返回 `null`。

**返回值**：`number | null` — 斜率值，或 `null`（垂直线无斜率）。

---

#### `toString(): string`

返回线段的字符串表示，格式为 `Line(Point(x1, y1), Point(x2, y2))`。

**返回值**：`string` — 如 `"Line(Point(1, 2), Point(3, 4))"`。

### 示例

```typescript
import { Point } from "./src/geometry/point.js";
import { Line } from "./src/geometry/line.js";

// 水平线
const horizontal = new Line(new Point(0, 0), new Point(5, 0));
console.log(horizontal.length()); // 5
console.log(horizontal.slope());  // 0

// 垂直线
const vertical = new Line(new Point(0, 0), new Point(0, 3));
console.log(vertical.length()); // 3
console.log(vertical.slope());  // null

// 斜线（3-4-5 直角三角形）
const diagonal = new Line(new Point(0, 0), new Point(3, 4));
console.log(diagonal.length()); // 5
console.log(diagonal.slope());  // 1.3333...

// 负斜率
const negSlope = new Line(new Point(0, 4), new Point(2, 0));
console.log(negSlope.slope()); // -2

console.log(new Line(new Point(1, 2), new Point(3, 4)).toString());
// "Line(Point(1, 2), Point(3, 4))"
```

---

## Circle

表示由圆心和半径定义的圆。

### 构造函数

```typescript
constructor(center: Point, radius: number)
```

| 参数     | 类型     | 说明                   |
|----------|----------|------------------------|
| `center` | `Point`  | 圆心坐标               |
| `radius` | `number` | 半径（必须为正数）     |

`center` 和 `radius` 均为只读属性（`readonly`）。

### 方法

#### `area(): number`

计算圆的面积（π × r²）。

**返回值**：`number` — 圆的面积。

---

#### `perimeter(): number`

计算圆的周长（2 × π × r）。

**返回值**：`number` — 圆的周长。

---

#### `contains(point: Point): boolean`

判断给定点是否在圆内（包含边界上的点）。

**参数**

| 参数    | 类型    | 说明         |
|---------|---------|--------------|
| `point` | `Point` | 待判断的点   |

**返回值**：`boolean` — 点在圆内（含边界）时返回 `true`，否则返回 `false`。

---

#### `toString(): string`

返回圆的字符串表示，格式为 `Circle(Point(cx, cy), r)`。

**返回值**：`string` — 如 `"Circle(Point(0, 0), 5)"`。

### 异常

| 条件              | 异常信息                    |
|-------------------|-----------------------------|
| `radius <= 0`     | `Error: "radius must be positive"` |

### 示例

```typescript
import { Point } from "./src/geometry/point.js";
import { Circle } from "./src/geometry/circle.js";

const center = new Point(0, 0);
const circle = new Circle(center, 5);

console.log(circle.area());      // 78.53981633974483 (π * 25)
console.log(circle.perimeter()); // 31.41592653589793 (2 * π * 5)

// 包含判断
console.log(circle.contains(new Point(0, 0))); // true  （圆心）
console.log(circle.contains(new Point(3, 0))); // true  （内部点）
console.log(circle.contains(new Point(5, 0))); // true  （边界点）
console.log(circle.contains(new Point(6, 0))); // false （外部点）
console.log(circle.contains(new Point(4, 4))); // false （对角外部，距离 ≈ 5.66）

console.log(new Circle(new Point(1, 2), 3).toString());
// "Circle(Point(1, 2), 3)"

// 异常：半径必须为正
try {
  new Circle(new Point(0, 0), -1);
} catch (e) {
  console.error(e.message); // "radius must be positive"
}
```

---

## Rectangle

表示由左上角坐标、宽度和高度定义的矩形（轴对齐）。

### 构造函数

```typescript
constructor(topLeft: Point, width: number, height: number)
```

| 参数      | 类型     | 说明                     |
|-----------|----------|--------------------------|
| `topLeft` | `Point`  | 矩形左上角坐标           |
| `width`   | `number` | 矩形宽度（必须为正数）   |
| `height`  | `number` | 矩形高度（必须为正数）   |

`topLeft`、`width`、`height` 均为只读属性（`readonly`）。

### 方法

#### `area(): number`

计算矩形的面积（width × height）。

**返回值**：`number` — 矩形面积。

---

#### `perimeter(): number`

计算矩形的周长（2 × (width + height)）。

**返回值**：`number` — 矩形周长。

---

#### `contains(point: Point): boolean`

判断给定点是否在矩形内（包含边界上的点）。

判断条件：`topLeft.x <= point.x <= topLeft.x + width` 且 `topLeft.y <= point.y <= topLeft.y + height`。

**参数**

| 参数    | 类型    | 说明         |
|---------|---------|--------------|
| `point` | `Point` | 待判断的点   |

**返回值**：`boolean` — 点在矩形内（含边界）时返回 `true`，否则返回 `false`。

---

#### `toString(): string`

返回矩形的字符串表示，格式为 `Rectangle(Point(x, y), width×height)`。

**返回值**：`string` — 如 `"Rectangle(Point(0, 0), 10×5)"`。

### 异常

| 条件              | 异常信息                      |
|-------------------|-----------------------------|
| `width <= 0`      | `Error: "width must be positive"`  |
| `height <= 0`     | `Error: "height must be positive"` |

### 示例

```typescript
import { Point } from "./src/geometry/point.js";
import { Rectangle } from "./src/geometry/rectangle.js";

const rect = new Rectangle(new Point(0, 0), 10, 5);

console.log(rect.area());      // 50
console.log(rect.perimeter()); // 30

// 包含判断
console.log(rect.contains(new Point(5, 2)));  // true  （内部点）
console.log(rect.contains(new Point(0, 0)));  // true  （左上角，边界包含）
console.log(rect.contains(new Point(10, 5))); // true  （右下角，边界包含）
console.log(rect.contains(new Point(11, 2))); // false （x 越界）
console.log(rect.contains(new Point(5, 6)));  // false （y 越界）

console.log(rect.toString()); // "Rectangle(Point(0, 0), 10×5)"

const r2 = new Rectangle(new Point(3, 4), 6, 2);
console.log(r2.toString()); // "Rectangle(Point(3, 4), 6×2)"

// 异常：宽度和高度必须为正
try {
  new Rectangle(new Point(0, 0), 0, 5);
} catch (e) {
  console.error(e.message); // "width must be positive"
}
try {
  new Rectangle(new Point(0, 0), 10, -2);
} catch (e) {
  console.error(e.message); // "height must be positive"
}
```

---

## Functions

### `area(shape: Shape): number`

多态面积计算函数，根据传入形状类型自动派发到对应的面积计算方法。

**参数**

| 参数    | 类型    | 说明                           |
|---------|---------|--------------------------------|
| `shape` | `Shape` | `Circle` 或 `Rectangle` 实例  |

**返回值**：`number` — 形状的面积。

```typescript
import { Point } from "./src/geometry/point.js";
import { Circle } from "./src/geometry/circle.js";
import { Rectangle } from "./src/geometry/rectangle.js";
import { area } from "./src/geometry/area.js";

const circle = new Circle(new Point(2, 3), 7);
console.log(area(circle)); // 153.93804002589985 (π * 49)

const rect = new Rectangle(new Point(1, 1), 8, 3);
console.log(area(rect)); // 24
```

---

### `circleArea(radius: number): number`

直接通过半径计算圆的面积（π × radius²），无需创建 `Circle` 实例。

**参数**

| 参数     | 类型     | 说明   |
|----------|----------|--------|
| `radius` | `number` | 圆半径 |

**返回值**：`number` — 圆的面积。

```typescript
import { circleArea } from "./src/geometry/area.js";

console.log(circleArea(5)); // 78.53981633974483
console.log(circleArea(1)); // 3.141592653589793
```

---

### `rectangleArea(width: number, height: number): number`

直接通过宽高计算矩形面积，无需创建 `Rectangle` 实例。

**参数**

| 参数     | 类型     | 说明     |
|----------|----------|----------|
| `width`  | `number` | 矩形宽度 |
| `height` | `number` | 矩形高度 |

**返回值**：`number` — 矩形面积（width × height）。

```typescript
import { rectangleArea } from "./src/geometry/area.js";

console.log(rectangleArea(8, 3)); // 24
console.log(rectangleArea(10, 5)); // 50
```

---

### `perimeter(shape: PerimeterShape): number`

多态周长计算函数，根据传入形状类型自动派发到对应的周长/长度计算方法。

- `Line`：返回线段长度（`line.length()`）
- `Circle`：返回圆周长（`circle.perimeter()`）
- `Rectangle`：返回矩形周长（`rectangle.perimeter()`）

**参数**

| 参数    | 类型             | 说明                                   |
|---------|------------------|----------------------------------------|
| `shape` | `PerimeterShape` | `Line`、`Circle` 或 `Rectangle` 实例  |

**返回值**：`number` — 形状的周长（或线段长度）。

```typescript
import { Point } from "./src/geometry/point.js";
import { Line } from "./src/geometry/line.js";
import { Circle } from "./src/geometry/circle.js";
import { Rectangle } from "./src/geometry/rectangle.js";
import { perimeter } from "./src/geometry/perimeter.js";

const line = new Line(new Point(0, 0), new Point(5, 0));
console.log(perimeter(line)); // 5

const circle = new Circle(new Point(2, 3), 7);
console.log(perimeter(circle)); // 43.982297150257104 (2 * π * 7)

const rect = new Rectangle(new Point(1, 1), 8, 3);
console.log(perimeter(rect)); // 22
```

---

### `lineLength(start, end): number`

直接通过两点坐标计算线段长度，无需创建 `Line` 实例。

**参数**

| 参数    | 类型                        | 说明       |
|---------|-----------------------------|------------|
| `start` | `{ x: number; y: number }` | 线段起点   |
| `end`   | `{ x: number; y: number }` | 线段终点   |

**返回值**：`number` — 两点之间的距离。

```typescript
import { lineLength } from "./src/geometry/perimeter.js";

console.log(lineLength({ x: 0, y: 0 }, { x: 3, y: 4 })); // 5
console.log(lineLength({ x: 0, y: 0 }, { x: 5, y: 0 })); // 5
```

---

### `circleCircumference(radius: number): number`

直接通过半径计算圆的周长（2 × π × radius），无需创建 `Circle` 实例。

**参数**

| 参数     | 类型     | 说明   |
|----------|----------|--------|
| `radius` | `number` | 圆半径 |

**返回值**：`number` — 圆的周长。

```typescript
import { circleCircumference } from "./src/geometry/perimeter.js";

console.log(circleCircumference(5)); // 31.41592653589793
console.log(circleCircumference(3)); // 18.84955592153876
```

---

### `rectanglePerimeter(width: number, height: number): number`

直接通过宽高计算矩形周长，无需创建 `Rectangle` 实例。

**参数**

| 参数     | 类型     | 说明     |
|----------|----------|----------|
| `width`  | `number` | 矩形宽度 |
| `height` | `number` | 矩形高度 |

**返回值**：`number` — 矩形周长（2 × (width + height)）。

```typescript
import { rectanglePerimeter } from "./src/geometry/perimeter.js";

console.log(rectanglePerimeter(10, 5)); // 30
console.log(rectanglePerimeter(8, 3));  // 22
```

---

## Types

### `Shape`

`Shape` 是面积计算支持的形状联合类型，定义于 `src/geometry/area.ts`。

```typescript
type Shape = Circle | Rectangle;
```

`Line` 不包含在内，因为线段没有面积的概念。

用于 `area(shape: Shape): number` 函数的参数类型。

---

### `PerimeterShape`

`PerimeterShape` 是周长计算支持的形状联合类型，定义于 `src/geometry/perimeter.ts`。

```typescript
type PerimeterShape = Line | Circle | Rectangle;
```

包含所有三种几何图形，因为线段长度、圆周长和矩形周长均可计算。

用于 `perimeter(shape: PerimeterShape): number` 函数的参数类型。
