using Random

function get_name()
    println("契約書だよ。そこに名前を書きな。")
    return readline()
end

function steal_name(name::String)
    chars = collect(name)
    index = rand(1:length(chars))
    return chars[index]
end

function yubaba_contract()
    name = get_name()
    println("フン。$(name)というのかい。贅沢な名だねぇ。")

    new_name = steal_name(name)
    println("今からお前の名前は$(new_name)だ。いいかい、$(new_name)だよ。分かったら返事をするんだ、$(new_name)!!")
end

yubaba_contract()
