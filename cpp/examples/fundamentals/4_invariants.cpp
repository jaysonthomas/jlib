struct Date 
{
    // Following members are public by default
    int month{1};
    int year{0};

    public:
        int Day() { return day; }
        void Day(int day) 
        { 
            this.day = day; 
        }

        // or
        void Day(int d) 
        { 
            if (d > 1)
                day = d;
            // Values < 1 are not accepted.
            // This limitation is called an invariant!
        }
    
    private:
        int day{1};
};
