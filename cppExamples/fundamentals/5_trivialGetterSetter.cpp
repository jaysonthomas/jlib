class Point
{
  int x;
  int y;

public:
  Point(int xx, int yy) : x{xx}, y{yy} {}

  int get_x() const // const here promises not to modify the object
  {
    return x;
  } 
  
  void set_x(int xx) 
  { 
    x = xx; 
  }
  
  int get_y() const 
  { 
    return y; 
  }
  
  void set_y(int yy) 
  { 
    y = yy; 
  }
};
