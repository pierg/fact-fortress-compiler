use dep::std;

mod data;

// BUG IN NOIR WITH MODULE OP., ISSUE POSTED ON GITHUB
fn custom_sum_(data: data::Data) -> [u8; data::SUM_SIZE]  {
    let mut result = [0; data::SUM_SIZE];
    for i in 0..data::DATA_SIZE {
        let mut index_1 = i as u8 % data::D1_SIZE as u8;
        let mut index_2 = i as u8 % data::D2_SIZE as u8;
        let sum = (data.d1[index_1 as Field] as u8 + data.d1[index_2 as Field] as u8) % 256;
        let mut index = i as u8 % data::SUM_SIZE as u8;
        result[index as Field] = (result[index as Field] as u8 + sum as u8) % 256;
        result[index as Field] = index;
    };
    result 
}

fn concatenate(data: data::Data) -> [u8; data::DATA_SIZE]  {
    let mut result = [0; data::DATA_SIZE];
    let mut cur_i = 0;
    for i in 0..data::D1_SIZE {
        result[cur_i] = data.d1[i];
        cur_i = cur_i + 1;
    }
    for i in 0..data::D2_SIZE {
        result[cur_i] = data.d2[i];
        cur_i = cur_i + 1;
    }
    result 
}