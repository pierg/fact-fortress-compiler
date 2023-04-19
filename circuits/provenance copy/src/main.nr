use dep::std;

mod data;

fn compute_function(data: data::Data) -> u8  {
    // TODO
    // Implement the function on the data...

    result 
}

fn main(
    public : pub data::Public,
    private : data::Private,
    ){

    // concatenate all the data
    let data = concatenate(private.data);

    // compute sha256
    let mut digest256 = std::sha256::digest(data);

    // proof of provenance and data consistency
    constrain std::schnorr::verify_signature(
        public.keys.x, 
        public.keys.y, 
        private.provenance.signature, 
        digest256) == 1;

    // compute function on the authenticated data
    let result = compute_function(private.data);

    // check that the result is consistent with the public statement
    constrain result == public.statement.value

}
