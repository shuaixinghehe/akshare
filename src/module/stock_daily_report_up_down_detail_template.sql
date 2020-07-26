select
    count(1) total_stock_cnt,
    cast(sum(if(convert(pct_chg,DECIMAL(5,2))>0.1,1,0)) as char) up_stock_cnt,

    group_concat(if(convert(pct_chg,DECIMAL(5,2))>0.1,ts_code,null)) up_stock_set,

    cast(sum(if(convert(pct_chg,DECIMAL(5,2))<-0.1,1,0)) as char) down_stock_cnt,
    group_concat(if(convert(pct_chg,DECIMAL(5,2))<-0.1,ts_code,null)) down_stock_set,

    cast(sum(if(convert(pct_chg,DECIMAL(5,2))>= -0.1 and convert(pct_chg,DECIMAL(5,2))<=0.1 ,1,0)) as char)  flat_stock_cnt,
    group_concat(if(convert(pct_chg,DECIMAL(5,2))>= -0.1 and convert(pct_chg,DECIMAL(5,2))<=0.1 ,ts_code,null)) flat_stock_set,



    cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=0.1 and convert(pct_chg,DECIMAL(5,2))< 1.0 ,1,0)) as char) up_0_1_stock_cnt,
    group_concat(if(convert(pct_chg,DECIMAL(5,2))>=0.1 and convert(pct_chg,DECIMAL(5,2))< 1.0,ts_code,null)) up_0_1_stock_set,


        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=1.0 and convert(pct_chg,DECIMAL(5,2))< 2.0 ,1,0)) as char) up_1_2_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=1.0 and convert(pct_chg,DECIMAL(5,2))<2.0,ts_code,null)) up_1_2_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=2.0 and convert(pct_chg,DECIMAL(5,2))< 3.0 ,1,0)) as char) up_2_3_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=2.0 and convert(pct_chg,DECIMAL(5,2))<3.0,ts_code,null)) up_2_3_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=3.0 and convert(pct_chg,DECIMAL(5,2))< 4.0 ,1,0)) as char) up_3_4_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=3.0 and convert(pct_chg,DECIMAL(5,2))<4.0,ts_code,null)) up_3_4_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=4.0 and convert(pct_chg,DECIMAL(5,2))< 5.0 ,1,0)) as char) up_4_5_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=4.0 and convert(pct_chg,DECIMAL(5,2))<5.0,ts_code,null)) up_4_5_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=5.0 and convert(pct_chg,DECIMAL(5,2))< 6.0 ,1,0)) as char) up_5_6_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=5.0 and convert(pct_chg,DECIMAL(5,2))<6.0,ts_code,null)) up_5_6_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=6.0 and convert(pct_chg,DECIMAL(5,2))< 7.0 ,1,0)) as char) up_6_7_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=6.0 and convert(pct_chg,DECIMAL(5,2))<7.0,ts_code,null)) up_6_7_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=7.0 and convert(pct_chg,DECIMAL(5,2))< 8.0 ,1,0)) as char) up_7_8_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=7.0 and convert(pct_chg,DECIMAL(5,2))<8.0,ts_code,null)) up_7_8_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=8.0 and convert(pct_chg,DECIMAL(5,2))< 9.0 ,1,0)) as char) up_8_9_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=8.0 and convert(pct_chg,DECIMAL(5,2))<9.0,ts_code,null)) up_8_9_stock_set,
    


        cast(sum(if(convert(pct_chg,DECIMAL(5,2))>=9.0 ,1,0)) as char) up_9_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))>=9.0 ,ts_code,null)) up_9_stock_set,




        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-0.1 and convert(pct_chg,DECIMAL(5,2))> -1.0 ,1,0)) as char) down_0_1_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-0.1 and convert(pct_chg,DECIMAL(5,2))>-1.0,ts_code,null)) down_0_1_stock_set,


        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-1.0 and convert(pct_chg,DECIMAL(5,2))> -2.0 ,1,0)) as char) down_1_2_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-1.0 and convert(pct_chg,DECIMAL(5,2))>-2.0,ts_code,null)) down_1_2_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-2.0 and convert(pct_chg,DECIMAL(5,2))> -3.0 ,1,0)) as char) down_2_3_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-2.0 and convert(pct_chg,DECIMAL(5,2))>-3.0,ts_code,null)) down_2_3_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-3.0 and convert(pct_chg,DECIMAL(5,2))> -4.0 ,1,0)) as char) down_3_4_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-3.0 and convert(pct_chg,DECIMAL(5,2))>-4.0,ts_code,null)) down_3_4_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-4.0 and convert(pct_chg,DECIMAL(5,2))> -5.0 ,1,0)) as char) down_4_5_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-4.0 and convert(pct_chg,DECIMAL(5,2))>-5.0,ts_code,null)) down_4_5_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-5.0 and convert(pct_chg,DECIMAL(5,2))> -6.0 ,1,0)) as char) down_5_6_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-5.0 and convert(pct_chg,DECIMAL(5,2))>-6.0,ts_code,null)) down_5_6_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-6.0 and convert(pct_chg,DECIMAL(5,2))> -7.0 ,1,0)) as char) down_6_7_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-6.0 and convert(pct_chg,DECIMAL(5,2))>-7.0,ts_code,null)) down_6_7_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-7.0 and convert(pct_chg,DECIMAL(5,2))> -8.0 ,1,0)) as char) down_7_8_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-7.0 and convert(pct_chg,DECIMAL(5,2))>-8.0,ts_code,null)) down_7_8_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-8.0 and convert(pct_chg,DECIMAL(5,2))> -9.0 ,1,0)) as char) down_8_9_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-8.0 and convert(pct_chg,DECIMAL(5,2))>-9.0,ts_code,null)) down_8_9_stock_set,
    

        cast(sum(if(convert(pct_chg,DECIMAL(5,2))<=-9.0 ,1,0)) as char) down_9_stock_cnt,
        group_concat(if(convert(pct_chg,DECIMAL(5,2))<=-9.0 ,ts_code,null)) down_9_stock_set
from stock_daily
where trade_date={};